"""Check exported fragments locally and against the public Hub page's CSS.

The Hub check changes only an isolated browser's DOM. It never saves or
publishes to ArcGIS, and cannot test the editor's HTML sanitizer.
"""

import json
from functools import partial
from html.parser import HTMLParser
from http.server import ThreadingHTTPServer
from threading import Thread

from playwright.sync_api import expect, sync_playwright

from check_browser import OUTPUT as CHECK_OUTPUT, ROOT, QuietHandler
from export_arcgis import HOME, MAP, OUTPUT, PARTS


class FragmentParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.ids = []
        self.links = []

    def handle_starttag(self, tag, attributes):
        values = dict(attributes)
        self.tags.append(tag)
        if "id" in values:
            self.ids.append(values["id"])
        for attribute in ("href", "src"):
            if attribute in values:
                self.links.append(values[attribute])


def main():
    checks = []
    fragments = []
    ids = []
    for name, _, _, _, suffix, background in PARTS:
        fragment = (OUTPUT / (name + ".html")).read_text(encoding="utf-8")
        parser = FragmentParser()
        parser.feed(fragment)
        assert not set(parser.tags).intersection({"html", "head", "body", "script", "svg", "path", "circle"}), name
        assert parser.tags.count("style") == (0 if suffix in ("header", "footer") else 1), name
        assert all(link.startswith(("https://", "#")) for link in parser.links), name
        ids.extend(parser.ids)
        fragments.append((fragment, suffix, background))
    assert len(ids) == len(set(ids)), "Duplicate IDs across exported sections"
    checks.append("fragment tags, style counts, absolute assets/home link, and unique IDs passed")
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(ROOT)))
    Thread(target=server.serve_forever, daemon=True).start()
    CHECK_OUTPUT.mkdir(exist_ok=True)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(channel="msedge", headless=True)
            try:
                page = browser.new_page()
                for width in (320, 390, 768, 1280):
                    page.set_viewport_size({"width": width, "height": 900})
                    page.goto(f"http://127.0.0.1:{server.server_port}/arcgis/homepage/preview.html")
                    page.wait_for_function("() => !!customElements.get('calcite-icon')")
                    page.wait_for_function("[...document.querySelectorAll('calcite-icon')].every(el => el.shadowRoot?.querySelector('svg'))")
                    page.evaluate("document.fonts.ready")
                    expect(page.locator("h1")).to_have_count(1)
                    page.locator(".topic-menu__toggle").click()
                    expect(page.locator(".topic-menu a")).to_have_count(3)
                    page.locator(".topic-menu__toggle").click()
                    page.locator(".question-directory__summary").click()
                    expect(page.locator(".question-group__links a")).to_have_count(12)
                    assert not page.evaluate("document.documentElement.scrollWidth > innerWidth"), width
                    page.screenshot(path=str(CHECK_OUTPUT / f"arcgis-assembly-{width}.png"), full_page=True)
                    checks.append(f"local assembly at {width}px passed, including four Calcite icons and dropdowns")

                page.set_viewport_size({"width": 1280, "height": 900})
                page.goto(HOME, wait_until="domcontentloaded")
                page.locator(".pinal-site-header").wait_for(timeout=45000)
                header = fragments[0][0]
                footer = fragments[-1][0]
                content = []
                for fragment, suffix, background in fragments[1:-1]:
                    style = f"background-color:{background};"
                    if suffix == "intro":
                        style += f"background-image:url('{MAP}');background-position:center;background-size:cover;"
                    content.append(f'<section class="layout-section" style="{style}"><div class="container-fluid"><div class="bs-row row"><div class="col-sm-12"><div class="markdown-card">{fragment}</div></div></div></div></section>')
                page.locator(".custom-header").evaluate("(el, html) => el.innerHTML = html", header)
                page.locator("#main-region").evaluate("(el, html) => el.innerHTML = html", "\n".join(content))
                page.locator(".custom-footer").evaluate("(el, html) => el.innerHTML = html", footer)
                page.add_style_tag(content=(OUTPUT / "01-header.css").read_text(encoding="utf-8"))
                page.add_style_tag(content=(OUTPUT / "06-footer.css").read_text(encoding="utf-8"))
                page.evaluate("document.fonts.ready")
                expected = {
                    ".hero h1": ("48px", "rgb(47, 74, 88)"),
                    ".hero .eyebrow": ("14px", "rgb(66, 119, 119)"),
                    ".topics .eyebrow": ("11px", "rgb(66, 119, 119)"),
                    ".topic-card__description": ("13px", "rgb(82, 103, 114)"),
                    ".about .eyebrow": ("11px", "rgb(66, 119, 119)"),
                    ".site-footer__links a": ("13px", "rgb(184, 218, 218)"),
                }
                for selector, (size, color) in expected.items():
                    computed = page.locator(selector).first.evaluate("el => ({size:getComputedStyle(el).fontSize, color:getComputedStyle(el).color})")
                    assert computed == {"size": size, "color": color}, (selector, computed)
                checks.append("source typography and colors retained against current public Hub styles")
                assert page.locator('.site-nav').evaluate("el => getComputedStyle(el).backgroundColor") == "rgba(0, 0, 0, 0)"
                assert page.locator('.topic-menu__toggle').evaluate("el => getComputedStyle(el).color") == "rgb(255, 255, 255)"
                checks.append("Hub navigation background override preserves readable white text on blue")
                page.locator(".topic-menu__toggle").click()
                link = page.locator(".topic-menu a").first
                assert link.evaluate("""el => {
                  const r = el.getBoundingClientRect();
                  return el.contains(document.elementFromPoint(r.x + r.width/2, r.y + r.height/2));
                }"""), "Hub shell clips or covers the navigation dropdown"
                page.locator(".topic-menu__toggle").click()
                page.locator(".question-directory__summary").click()
                for width in (390, 1280):
                    page.set_viewport_size({"width": width, "height": 900})
                    assert not page.evaluate("document.documentElement.scrollWidth > innerWidth"), width
                    page.evaluate("window.scrollTo(0, 0)")
                    page.screenshot(path=str(CHECK_OUTPUT / f"arcgis-public-shell-{width}.png"), full_page=True)
                    checks.append(f"read-only public Hub CSS assembly at {width}px passed")
                page.locator('.site-footer a[href="#"]').click()
                page.wait_for_function("window.scrollY < 2")
                checks.append("Back to top works with Hub's fixed header")
                checks.append("no ArcGIS save or publish requests made; editor sanitization remains untested")
                page.close()
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()
    (CHECK_OUTPUT / "arcgis-export-results.json").write_text(json.dumps(checks, indent=2), encoding="utf-8")
    print(json.dumps(checks, indent=2))


if __name__ == "__main__":
    main()
