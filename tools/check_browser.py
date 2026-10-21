"""Confirm local browser automation works; this is not a full accessibility audit."""

import argparse
import json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from playwright.sync_api import expect, sync_playwright


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / ".browser-checks"


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--browser", choices=("msedge", "chrome"), default="msedge")
    channel = parser.parse_args().browser
    OUTPUT.mkdir(exist_ok=True)
    server = ThreadingHTTPServer(
        ("127.0.0.1", 0), partial(QuietHandler, directory=str(ROOT))
    )
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    results = []
    try:
        with sync_playwright() as playwright:
            # Edge uses a temporary profile, separate from your everyday browser.
            browser = playwright.chromium.launch(channel=channel, headless=True)
            try:
                for name, width in (("desktop", 1280), ("phone", 390)):
                    context = browser.new_context(viewport={"width": width, "height": 900})
                    try:
                        page = context.new_page()
                        page_errors = []
                        page.on("pageerror", lambda error: page_errors.append(str(error)))
                        response = page.goto(
                            f"http://127.0.0.1:{server.server_port}/index.html",
                            wait_until="load",
                        )
                        assert response.status == 200, "Homepage did not load"
                        fonts_ready = page.evaluate("""() => Promise.race([
                            document.fonts.ready.then(() => true),
                            new Promise(resolve => setTimeout(() => resolve(false), 10000))
                        ])""")
                        navigation = page.locator(".topic-menu")
                        toggle = page.locator(".topic-menu__toggle")
                        expect(navigation).not_to_have_attribute("open", "")
                        toggle.focus()
                        page.keyboard.press("Enter")
                        expect(navigation).to_have_attribute("open", "")
                        expect(navigation.get_by_role("link", name="Economic Indicators", exact=True)).to_be_visible()
                        page.screenshot(path=str(OUTPUT / f"{channel}-{name}-navigation.png"), full_page=True)
                        page.keyboard.press("Space")
                        expect(navigation).not_to_have_attribute("open", "")

                        questions = page.locator(".question-directory__disclosure")
                        page.locator(".question-directory__summary").focus()
                        page.keyboard.press("Enter")
                        expect(questions).to_have_attribute("open", "")
                        expect(questions.get_by_role("link")).to_have_count(12)
                        page.screenshot(path=str(OUTPUT / f"{channel}-{name}-questions.png"), full_page=True)
                        overflow = page.evaluate(
                            "document.documentElement.scrollWidth > window.innerWidth"
                        )
                        images_ok = page.locator("img").evaluate_all(
                            "images => images.every(image => image.complete && image.naturalWidth > 0)"
                        )
                        assert not overflow, f"Horizontal overflow at {width}px"
                        assert images_ok, "An HTML image did not load"
                        assert not page_errors, page_errors
                        results.append({
                            "browser": channel,
                            "viewport": name,
                            "width": width,
                            "keyboard_disclosures": "passed",
                            "horizontal_overflow": overflow,
                            "html_images_loaded": images_ok,
                            "font_wait_completed": fonts_ready,
                        })
                    finally:
                        context.close()
            finally:
                browser.close()
        (OUTPUT / f"{channel}-results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
        print(json.dumps({"checks": results, "screenshots": str(OUTPUT)}, indent=2))
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


if __name__ == "__main__":
    main()
