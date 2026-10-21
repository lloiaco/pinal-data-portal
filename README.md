# Pinal County Economic & Workforce Data Portal

A multipage portal developed incrementally with plain HTML and CSS. GitHub Pages will provide development previews; ArcGIS Hub remains the work publishing destination. See [PROJECT_BRIEF.md](PROJECT_BRIEF.md) for decisions and proposals.

## Current increment

The local homepage contains the header, introduction, four topic cards, question dropdown, About section, and footer. Its logo, fonts, blue-and-gold header, and topic-card pattern come from the existing site. The supplied `Pinal Map.png` provides the introductory background; the published source references a different image resource, so this is a local adaptation rather than a verified visual match.

The header has a linked County logo and portal name plus one "Explore topics" dropdown, replacing the three homepage section links. It uses native `details`/`summary`, starts closed, and links to the live Economic Indicators, Workforce Performance, and H3 pages. Targeted Industries appears as non-linked text marked "In development". On desktop the dropdown appears beneath its toggle; on narrow screens it expands within the header. Click the toggle again to close it. Breadcrumbs will be added when interior pages are developed.

Three topic cards also link to their live topic pages. Targeted Industries has an "In development" status rather than a placeholder link; its separate promotional section is skipped at the owner's request. About and the footer use the existing homepage's wording and links, with Department Home updated to the County's current URL. About uses Pinal cream with the updated dark-teal eyebrow. The footer includes Department Home, Accessibility, and Back to top, with wrapping layout for smaller screens. Verification results are recorded below.

The question section is one dropdown, closed by default, containing grouped question links in two columns and one column on narrow screens. Its blue header restores the published site's style: "Not sure where to begin?", the shorter heading "Start with the question", and "Browse Questions" with a circular plus on the right. The plus becomes a minus when expanded. The header wraps on narrow screens. The source site's pale teal (`#b8dada`) is named `pinal-teal-light` and reused for accents on blue; interior links remain dark teal on white.

HTML `<details>` supplies the expandable container and `<summary>` its clickable header, without JavaScript. The summary has visible keyboard focus and can be toggled with Enter or Space. Available questions are underlined links, without individual dropdowns, cards, or answer descriptions. Questions describe reader interests and may intentionally share a destination. Economic Indicators, Workforce Performance, and H3 each have four linked questions. The owner confirmed that population projections are available. Workforce Performance links directly to the two existing branches supplied in the brief. Targeted Industries has three planned questions as plain text beneath its development note.

The cards use CSS Grid: four columns on wide screens, two at 1,000 pixels and below, and one at 700 pixels and below (with the default browser text size). Each card uses Flexbox vertically; `margin-top: auto` places its link at the bottom without a fixed height. Decorative inline SVG icons need no JavaScript or icon library. Card labels are larger than the live source's tiny labels, and the Economic Indicators description follows the indicator inventory recorded in the brief.

## Preview and edit

1. Open this repository folder in VS Code.
2. Find `index.html` in the Explorer, right-click it, and choose **Reveal in File Explorer**.
3. Double-click `index.html` in File Explorer to open it in your browser.
4. Edit a file in VS Code, save it, then refresh the browser.

No installation, framework, build tool, or local server is required for this increment. The two Roboto font families load from Google Fonts when online; system fonts provide fallbacks. All project file paths are relative so the page also works beneath GitHub Pages' `/pinal-data-portal/` path.

To check the layout, resize your browser to a narrow phone width, then use Tab to move through the skip link, brand, and Explore topics toggle. Use Enter or Space to expand it, Tab through the three links, and return to the toggle to close it. Closed links should be skipped in the Tab order. At narrow widths, navigation moves below the brand. Browser verification and ArcGIS verification should be recorded separately from source checks.

## Browser testing setup

Playwright for Python is installed in the local `.venv` environment and controls the existing Microsoft Edge installation in an isolated, headless session. No Node.js installation or website build step is required. This is script-driven browser automation, rather than a connected interactive browser tool in the chat.

Run the initial browser check from the repository's VS Code terminal:

```powershell
.\.venv\Scripts\python.exe tools/check_browser.py
```

The script starts a temporary server on `127.0.0.1`, opens the homepage at 1280px and 390px widths, operates the dropdowns with Enter and Space, checks for horizontal overflow and broken HTML images, and captures screenshots. It closes its browser and server when finished. Results and four screenshots are saved in `.browser-checks/`. That folder and `.venv/` are excluded from Git.

To reproduce the testing setup on another Windows computer with Python and Edge installed:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

The initial run passed at both widths on October 21, 2026. The later verification below expands that coverage. Add `--browser chrome` to run the basic check in installed Chrome. Output filenames include the browser channel, such as `msedge-results.json` or `chrome-results.json`. The basic script's font-wait result only indicates waiting completed; the full verification also checks that the two font families are available.

## Homepage verification — October 21, 2026

The full verification script completed 81 checks: 79 passed, none failed, and two public County links were inconclusive because both HTTP requests and automated Edge received a Cloudflare 403 response. Their content was independently retrieved through the web reader; this does not establish access from every visitor's browser.

| Check | Result |
| --- | --- |
| Edge layout at 320, 360, 390, 700, 768, 800, 1000, 1024, 1280, and 1920px | No horizontal overflow or checked text elements outside the viewport, with dropdowns closed and expanded. |
| Native Edge zoom at 100%, 200%, and 400% in an isolated profile | Zoom confirmed by browser metrics; layout passed. 200% and 400% viewport screenshots inspected. |
| 200% root text size and increased line/letter/word/paragraph spacing | Passed at narrow and desktop widths; these stress tests are separate from native zoom. |
| Keyboard at 390px and 1280px | Tab order, skip link, visible focus outlines, disclosure activation/closing, all 12 question links, and navigation into the footer passed. Hidden disclosure links were skipped. |
| Browser accessibility tree | Both disclosures expose names and expanded/collapsed states. This is not a screen-reader listening test. |
| axe-core 4.11.4, closed and expanded views | Zero reported violations across applicable WCAG A/AA rules through 2.2 plus best practices. It requested contrast review for five decorative arrow spans in each state; source review and the color-pair calculations cover their inherited colors. |
| Text contrast | All eight used text/background combinations tested passed the 4.5:1 ordinary-text threshold. No gold heading text remains. |
| Forced-colors mode | No layout overflow; screenshot captured. It still needs a human usability review in that mode. |
| Chrome at 1280px and 390px | Basic dropdown keyboard, image-loading, and overflow checks passed. |
| Local paths, anchors, IDs, heading structure, fonts, and GitHub Pages project subpath | Passed, including loading the page and its local resources under `/pinal-data-portal/`. |
| Five distinct ArcGIS link destinations | HTTP 200 and expected page titles/content. Tableau interaction and underlying data were not audited. |
| County footer links | Department Home updated from the redirecting `/1088/` URL to [the current `/1849/` page](https://www.pinal.gov/1849/Economic-Workforce-Development). Both this and [Accessibility](https://www.pinal.gov/153/Accessibility) block automated HTTP/browser checks; independently readable through the web reader. |

Run the full verification from the repository terminal:

```powershell
.\.venv\Scripts\python.exe tools/verify_homepage.py
```

It downloads the pinned axe checker into ignored `.browser-checks/` on its first run, uses installed Edge, reads public link destinations, and writes `verification.json`, an accessibility-tree snapshot, and screenshots there. axe is testing software only and is not loaded by the website. Native zoom captures use viewport screenshots because Playwright full-page screenshots can crop at native zoom levels.

Screen-reader announcements are untested at the owner's request. Safari and Firefox were not tested. ArcGIS Hub integration and the actual GitHub Pages deployment require checks in those environments later. Automated results do not establish full accessibility conformance. Per the owner's instruction, no commit, push, or GitHub Pages configuration was performed; those steps will be done by the owner with guidance.

References: [Playwright Python installation](https://playwright.dev/python/docs/intro), [using installed Edge](https://playwright.dev/python/docs/browsers#google-chrome--microsoft-edge).

## Files and responsibilities

| File | Purpose |
| --- | --- |
| `index.html` | Page content, meaningful HTML structure, and links. |
| `css/pinal-theme.css` | County colors, fonts, image choice, and purpose-based design values. |
| `css/components.css` | Reusable layout, header, introduction, topic cards, question dropdown, About, footer, responsive rules, and keyboard focus styling. |
| `css/arcgis-compat.css` | Reserved for documented Hub adjustments; currently comments only. |
| `images/` | Owner-supplied images, with original filenames preserved. |

Load the theme before the components and compatibility file. The `.data-portal` class scopes the styles: it is on the standalone page's body and will need a wrapper around exported text-card content.

## Learning the color system

CSS custom properties are named values. For example:

```css
--pinal-blue: #2f4a58;
--color-text: var(--pinal-blue);
```

`pinal-blue` identifies the brand color. `color-text` describes its purpose. A component uses `color: var(--color-text)` so it can be reused with another theme.

| Palette name | Value | Intended use |
| --- | --- | --- |
| `pinal-blue` | `#2f4a58` | Main text, header background, focus on light backgrounds. |
| `pinal-teal` | `#549898` | Topic-card top borders and active borders. |
| `pinal-gold` | `#d29040` | Header border and navigation hover/focus accent. |
| `pinal-tan` | `#d6cbaf` | Card and status borders. |
| `pinal-teal-dark` | `#427777` | Eyebrows, card labels, and links on white or Pinal cream. |
| `pinal-teal-light` | `#b8dada` | Eyebrow and disclosure control on the blue question header. |
| `pinal-sand` | `#f1ede3` | Warm section background, reserved for later sections. |
| `pinal-cream` | `#fcfaf6` | Soft background and text on the blue header. |
| `neutral-white` | `#ffffff` | Page background. |

Transparency and shadows use those palette colors. Dark teal was updated from `#477f7f` to `#427777`, providing about 4.87:1 contrast on Pinal cream and 5.08:1 on white. The introductory panel remains solid white. The hero description uses Pinal blue. Card descriptions use the existing site's softer slate (`#526772`), named `pinal-slate` and applied through `color-text-muted`.

The typography hierarchy uses a 0.875rem hero eyebrow (14px at the default root size), 0.6875rem section eyebrow (11px), 0.6875rem card label (11px), and 0.8125rem card description (13px). These are explicit visual tiers rather than automatic proportions of the following headings. Smaller card labels carry supporting context; the topic names remain larger headings.

Source checks confirmed that local files and anchors resolve and that the CSS custom properties are defined. Blue text on white measures about 9.37:1; cream text on the blue header measures about 8.99:1. These contrast calculations do not replace browser, keyboard, mobile, or ArcGIS Hub verification, which remain pending.

## Accessibility reference

Follow the [County accessibility guidance](https://www.pinal.gov/153/Accessibility), which references Section 508 and WCAG 2.0 Levels A and AA. The brief records the development requirements and verification limits.

The current source includes meaningful headings, descriptive links, keyboard focus styling, a skip link, decorative-image handling, and a County accessibility link in the footer. Browser appearance approval does not establish accessibility conformance. Check keyboard operation, visible focus, text resizing to 200%, and screen-reader behavior as the page develops. Include Tableau content and the ArcGIS Hub environment in later reviews.

## Maintaining shared content

Styles are shared through the same CSS files. Header HTML currently lives in `index.html`; there is only one local page, so automatic header/footer inclusion is not needed yet. Before adding another page, choose and document how shared markup will be maintained. No JavaScript injection or build system has been introduced.

When a page is complete and the owner requests it, prepare its sections for ArcGIS Hub text cards. Hub row settings, shared headers, asset URLs, and CSS behavior require their own verification.
