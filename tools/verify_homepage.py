"""Reproducible homepage checks. Results are evidence, not a conformance claim."""

import base64
import hashlib
import json
import re
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from http.server import ThreadingHTTPServer
from threading import Thread
from urllib.parse import unquote
from urllib.request import Request, urlopen

from playwright.sync_api import sync_playwright

from check_browser import OUTPUT, ROOT, QuietHandler

AXE_URL = "https://cdn.jsdelivr.net/npm/axe-core@4.11.4/axe.min.js"
checks = []


def record(name, passed, detail=None):
    checks.append({"name": name, "passed": None if passed is None else bool(passed), "detail": detail})


def luminance(color):
    channels = [int(color[index:index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4 for value in channels]
    return sum(value * weight for value, weight in zip(linear, (0.2126, 0.7152, 0.0722)))


def contrast(foreground, background):
    values = sorted((luminance(foreground), luminance(background)))
    return (values[1] + 0.05) / (values[0] + 0.05)


def fetch_link(url):
    try:
        with urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=40) as response:
            html = response.read().decode("utf-8", errors="replace")
            title = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
            result = {"url": url, "status": response.status, "final_url": response.url,
                      "title": title.group(1).strip() if title else ""}
            injected = re.search(r'window\.__SITE="([^"]+)"', html)
            if injected:
                data = json.loads(unquote(injected.group(1)))
                result["arcgis_status"] = data.get("status")
                site = data.get("site", {})
                result["item_title"] = site.get("item", {}).get("title")
                layout = site.get("data", {}).get("values", {}).get("layout", {})
                cards = [card.get("component", {}).get("settings", {}).get("markdown", "")
                         for section in layout.get("sections", [])
                         for row in section.get("rows", []) for card in row.get("cards", [])]
                text = re.sub(r"<style.*?</style>", "", "\n".join(cards), flags=re.S | re.I)
                text = re.sub(r"<[^>]+>", " ", text)
                result["content_excerpt"] = re.sub(r"\s+", " ", text).strip()[:8000]
            return result
    except Exception as error:
        return {"url": url, "error": str(error)}


def layout_check(page, label):
    issues = page.evaluate("""() => ({
      overflow: document.documentElement.scrollWidth > innerWidth + 1,
      outside: [...document.querySelectorAll('main p, main h1, main h2, main h3, main a, header a, header summary, footer a')]
        .filter(el => el.getClientRects().length && (el.getBoundingClientRect().left < -1 || el.getBoundingClientRect().right > innerWidth + 1))
        .map(el => el.textContent.trim().slice(0, 90))
    })""")
    record(label, not issues["overflow"] and not issues["outside"], issues)


def focus_info(page):
    return page.evaluate("""() => {
      const el = document.activeElement, css = getComputedStyle(el);
      return {tag: el.tagName, text: el.textContent.trim().replace(/\\s+/g, ' ').slice(0, 120),
        id: el.id, class: el.className, href: el.getAttribute('href'),
        visibleFocus: el.matches(':focus-visible') && css.outlineStyle !== 'none' && parseFloat(css.outlineWidth) >= 2};
    }""")


def main():
    OUTPUT.mkdir(exist_ok=True)
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    ids = re.findall(r'\bid="([^"]+)"', html)
    record("unique IDs", len(ids) == len(set(ids)))
    missing = []
    for reference in re.findall(r'(?:href|src)="([^"]+)"', html):
        if reference.startswith("http"):
            continue
        if reference.startswith("#"):
            if reference[1:] not in ids:
                missing.append(reference)
        elif not (ROOT / unquote(reference)).is_file():
            missing.append(reference)
    record("local paths and fragment targets", not missing, missing)
    record("heading structure", len(re.findall(r'<h1\b', html)) == 1)

    axe_path = OUTPUT / "axe-4.11.4.min.js"
    if not axe_path.exists():
        with urlopen(AXE_URL, timeout=40) as response:
            axe_path.write_bytes(response.read())
    axe_hash = hashlib.sha256(axe_path.read_bytes()).hexdigest()

    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(ROOT)))
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}/index.html"
    axe_results = []
    keyboard_results = []
    county_browser_links = []
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(channel="msedge", headless=True)
            try:
                for width in (320, 360, 390, 700, 768, 800, 1000, 1024, 1280, 1920):
                    page = browser.new_page(viewport={"width": width, "height": 900})
                    page.goto(base)
                    page.evaluate("document.fonts.ready")
                    layout_check(page, f"layout {width}px, dropdowns closed")
                    page.locator(".topic-menu__toggle").click()
                    layout_check(page, f"layout {width}px, navigation open")
                    page.locator(".topic-menu__toggle").click()
                    page.locator(".question-directory__summary").click()
                    layout_check(page, f"layout {width}px, questions open")
                    if width in (320, 768, 1280):
                        page.screenshot(path=str(OUTPUT / f"audit-{width}.png"), full_page=True)
                    page.close()

                page = browser.new_page(viewport={"width": 1280, "height": 900})
                page.goto(base)
                page.evaluate("document.fonts.ready")
                fonts = page.evaluate("""() => ({body: document.fonts.check('400 16px Roboto'),
                    heading: document.fonts.check('600 32px "Roboto Condensed"')})""")
                record("Google Fonts loaded", all(fonts.values()), fonts)
                for state in ("closed", "both-open"):
                    if state == "both-open":
                        page.locator("details").evaluate_all("items => items.forEach(el => el.open = true)")
                    page.add_script_tag(path=str(axe_path))
                    result = page.evaluate("""async () => {
                      const result = await axe.run(document, {runOnly: {type: 'tag',
                        values: ['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa','best-practice']}});
                      return {violations: result.violations, incomplete: result.incomplete,
                        passedRules: result.passes.length, version: result.testEngine.version};
                    }""")
                    axe_results.append({"state": state, **result})
                    record(f"axe accessibility scan {state}", not result["violations"],
                           [item["id"] for item in result["violations"]])
                (OUTPUT / "accessibility-tree.txt").write_text(page.locator("body").aria_snapshot(), encoding="utf-8")

                for width in (390, 1280):
                    page.set_viewport_size({"width": width, "height": 900})
                    page.goto(base)
                    sequence = []
                    for _ in range(10):
                        page.keyboard.press("Tab")
                        sequence.append(focus_info(page))
                    expected = ["skip-link", "site-brand", "topic-menu__toggle", "topic-card__link",
                                "topic-card__link", "topic-card__link", "question-directory__summary",
                                None, None, None]
                    sequence_ok = all(
                        item["class"] == wanted if wanted else item["tag"] == "A"
                        for item, wanted in zip(sequence, expected)
                    )
                    record(f"closed-dropdown Tab order at {width}px", sequence_ok, sequence)
                    record(f"keyboard focus outlines at {width}px", all(item["visibleFocus"] for item in sequence))
                    keyboard_results.append({"width": width, "closed_sequence": sequence})

                    page.goto(base)
                    page.keyboard.press("Tab")
                    page.screenshot(path=str(OUTPUT / f"skip-focus-{width}.png"))
                    page.keyboard.press("Enter")
                    record(f"skip link moves focus into main at {width}px", page.evaluate("document.activeElement.id") == "main-content")
                    page.keyboard.press("Tab")
                    record(f"Tab after skip reaches first content link at {width}px", focus_info(page)["class"] == "topic-card__link")

                    toggle = page.locator(".topic-menu__toggle")
                    toggle.focus()
                    page.keyboard.press("Enter")
                    nav_links = []
                    for _ in range(3):
                        page.keyboard.press("Tab")
                        nav_links.append(focus_info(page))
                    record(f"open topic dropdown has three focused links at {width}px",
                           all(item["tag"] == "A" and item["visibleFocus"] for item in nav_links), nav_links)
                    toggle.focus()
                    page.keyboard.press("Space")
                    record(f"Space closes topic dropdown at {width}px", not page.locator(".topic-menu").evaluate("el => el.open"))
                    page.locator(".question-directory__summary").focus()
                    page.keyboard.press("Enter")
                    questions = []
                    for _ in range(12):
                        page.keyboard.press("Tab")
                        questions.append(focus_info(page))
                    record(f"all twelve questions keyboard reachable at {width}px",
                           all(item["tag"] == "A" and item["visibleFocus"] for item in questions), questions)
                    page.keyboard.press("Tab")
                    record(f"Tab exits questions into footer at {width}px", focus_info(page)["text"] == "Department Home")

                # Explicit text-resize stress test, not a substitute for native browser zoom.
                for width in (390, 1280):
                    page.set_viewport_size({"width": width, "height": 900})
                    page.goto(base)
                    page.evaluate("document.documentElement.style.fontSize = '200%'")
                    page.locator("details").evaluate_all("items => items.forEach(el => el.open = true)")
                    layout_check(page, f"200% root text size at {width}px")
                    page.screenshot(path=str(OUTPUT / f"text200-{width}.png"), full_page=True)
                page.close()
                # Confirm semantic state is exposed to assistive technology APIs.
                semantic_page = browser.new_page()
                semantic_page.goto(base)
                session = semantic_page.context.new_cdp_session(semantic_page)
                for expanded in (False, True):
                    semantic_page.locator("details").evaluate_all(
                        "(items, expanded) => items.forEach(item => item.open = expanded)", expanded)
                    tree = session.send("Accessibility.getFullAXTree")["nodes"]
                    disclosures = [node for node in tree if node.get("role", {}).get("value") == "DisclosureTriangle"]
                    record(f"native disclosure accessibility state expanded={expanded}",
                           len(disclosures) == 2 and all(
                               node.get("name", {}).get("value") and any(
                                   prop.get("name") == "expanded" and prop.get("value", {}).get("value") == expanded
                                   for prop in node.get("properties", [])) for node in disclosures))

                for width in (320, 1280):
                    semantic_page.set_viewport_size({"width": width, "height": 900})
                    semantic_page.goto(base)
                    semantic_page.add_style_tag(content="""
                      .data-portal * {line-height: 1.5 !important; letter-spacing: .12em !important; word-spacing: .16em !important;}
                      .data-portal p {margin-bottom: 2em !important;}
                    """)
                    semantic_page.locator("details").evaluate_all("items => items.forEach(el => el.open = true)")
                    layout_check(semantic_page, f"increased text-spacing at {width}px")
                    semantic_page.screenshot(path=str(OUTPUT / f"text-spacing-{width}.png"), full_page=True)
                semantic_page.emulate_media(forced_colors="active")
                semantic_page.goto(base)
                semantic_page.locator("details").evaluate_all("items => items.forEach(el => el.open = true)")
                layout_check(semantic_page, "forced-colors layout")
                semantic_page.screenshot(path=str(OUTPUT / "forced-colors.png"), full_page=True)
                semantic_page.close()

                # Serve from a project subpath, as GitHub Pages will do.
                pages_server = ThreadingHTTPServer(
                    ("127.0.0.1", 0), partial(QuietHandler, directory=str(ROOT.parent)))
                Thread(target=pages_server.serve_forever, daemon=True).start()
                try:
                    pages_page = browser.new_page()
                    local_failures = []
                    pages_page.on("response", lambda response: local_failures.append(response.url)
                                  if response.url.startswith("http://127.0.0.1") and response.status >= 400 else None)
                    pages_response = pages_page.goto(
                        f"http://127.0.0.1:{pages_server.server_port}/pinal-data-portal/index.html")
                    record("GitHub Pages project-path resources", pages_response.status == 200 and not local_failures, local_failures)
                    pages_page.close()
                finally:
                    pages_server.shutdown()
                    pages_server.server_close()

                # Public County pages may block simple HTTP clients. Try real Edge too.
                for url in ("https://www.pinal.gov/1849/Economic-Workforce-Development",
                            "https://www.pinal.gov/153/Accessibility"):
                    link_page = browser.new_page()
                    try:
                        response = link_page.goto(url, wait_until="domcontentloaded", timeout=40000)
                        county_browser_links.append({"url": url, "status": response.status,
                                                     "final_url": link_page.url, "title": link_page.title()})
                    except Exception as error:
                        county_browser_links.append({"url": url, "error": str(error)})
                    finally:
                        link_page.close()
            finally:
                browser.close()

            # Native browser zoom in a testing profile, never the user's everyday profile.
            zoom_context = playwright.chromium.launch_persistent_context(
                str(OUTPUT / "verification-zoom-profile"), channel="msedge", headless=True,
                no_viewport=True, args=["--window-size=1280,900"])
            try:
                zoom_page = zoom_context.pages[0]
                for scale in (1, 2, 4):
                    zoom_page.goto("edge://settings/appearance")
                    zoom_page.evaluate("scale => chrome.settingsPrivate.setDefaultZoom(scale)", scale)
                    zoom_page.goto(base)
                    zoom_page.evaluate("document.fonts.ready")
                    zoom_page.locator("details").evaluate_all("items => items.forEach(el => el.open = true)")
                    metrics = zoom_page.evaluate("({innerWidth, outerWidth, devicePixelRatio})")
                    record(f"native browser zoom {scale * 100}% applied", abs(metrics["devicePixelRatio"] - scale) < 0.01, metrics)
                    layout_check(zoom_page, f"native browser zoom {scale * 100}% layout")
                    # Native browser zoom can crop Playwright's full-page capture.
                    # DevTools viewport capture preserves the physical browser width.
                    zoom_page.evaluate("window.scrollTo(0, 0)")
                    capture = zoom_context.new_cdp_session(zoom_page).send("Page.captureScreenshot", {"format": "png"})
                    (OUTPUT / f"native-zoom{scale * 100}-viewport.png").write_bytes(base64.b64decode(capture["data"]))
            finally:
                zoom_context.close()
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)

    pairs = [("blue on white", "#2f4a58", "#ffffff"), ("blue on cream", "#2f4a58", "#fcfaf6"),
             ("dark teal on white", "#427777", "#ffffff"), ("dark teal on cream", "#427777", "#fcfaf6"),
             ("slate on white", "#526772", "#ffffff"), ("slate on cream", "#526772", "#fcfaf6"),
             ("white on blue", "#ffffff", "#2f4a58"), ("pale teal on blue", "#b8dada", "#2f4a58")]
    for label, foreground, background in pairs:
        ratio = contrast(foreground, background)
        record(f"ordinary text contrast: {label}", ratio >= 4.5, round(ratio, 4))
    urls = sorted(set(re.findall(r'<a[^>]+href="(https://[^"]+)"', html)))
    with ThreadPoolExecutor(max_workers=4) as pool:
        links = list(pool.map(fetch_link, urls))
    for link in links:
        browser_link = next((item for item in county_browser_links if item["url"] == link["url"]), None)
        success = link.get("status") == 200 and link.get("arcgis_status", 200) == 200
        if browser_link and browser_link.get("status") == 200:
            success = True
        blocked = "403" in link.get("error", "") or (browser_link and browser_link.get("status") == 403)
        record(f"external link: {link['url']}", True if success else None if blocked else False,
               {"http_client": {key: value for key, value in link.items() if key != "content_excerpt"},
                "browser": browser_link})
    result = {"checks": checks, "axe": axe_results, "axe_url": AXE_URL, "axe_sha256": axe_hash,
              "external_links": links, "keyboard": keyboard_results,
              "not_tested": ["actual screen-reader announcements", "ArcGIS Hub integration"]}
    (OUTPUT / "verification.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    failed = [item for item in checks if item["passed"] is False]
    print(json.dumps({"total": len(checks), "failed": failed,
        "inconclusive": [item for item in checks if item["passed"] is None], "axe_incomplete": [
        {"state": entry["state"], "rules": [item["id"] for item in entry["incomplete"]]}
        for entry in axe_results], "report": str(OUTPUT / "verification.json")}, indent=2))
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
