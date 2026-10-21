# Pinal County Economic & Workforce Data Portal

Recorded October 21, 2026. This brief preserves the project decisions and proposed direction from the planning conversation.

## Confirmed decisions

- Repository: [lloiaco/pinal-data-portal](https://github.com/lloiaco/pinal-data-portal).
- Keep the entire multipage portal in one repository.
- Use VS Code and GitHub for development, with GitHub Pages as the development and preview environment. ArcGIS Hub remains the required publishing destination for these work pages.
- Begin with portable, reusable HTML and CSS outside ArcGIS Hub; add JavaScript where needed.
- Discuss any proposed framework or build tool before introducing it.
- Keep reusable component styles, Pinal branding, and ArcGIS Hub compatibility adjustments separate.
- Use shared styling and maintainable headers, navigation, and footers.
- Support phones and desktops.
- Preserve the four main portal topics and establish consistent site navigation and breadcrumbs.
- Review the existing visual design before replacing it; the owner likes much of its current styling.
- Develop incrementally, with focused changes and explanations of important decisions so the owner can learn.
- Establish the project structure and shared design approach before developing the homepage and Activity and Outcomes branch incrementally.
- Do not build the entire portal immediately.
- Dashboards are embedded Tableau products. Hosting the surrounding website on GitHub Pages does not migrate those dashboards or remove their hosting dependencies.
- Develop complete pages in the repository first. When the owner requests it, break a completed page into sections suitable for ArcGIS Hub text cards.
- Keep ArcGIS Hub constraints in mind throughout development; compatibility must be checked rather than assumed.
- Teach transferable web design and coding skills. The owner wants reusable methods and a development system they can continue using beyond this job, potentially for consulting or other businesses. Keep general techniques separate from County-specific branding and content.

## Audience

The portal is a public information resource for Pinal County Economic and Workforce Development. No single primary audience has been established.

- Economic Indicators: expected to serve the public broadly; this is an assumption, not measured visitor behavior.
- Workforce Performance: board members may be a likely audience, but this is uncertain.
- H3 Occupation Analysis: known users include Central Arizona College for program research and the owner's supervisor and colleagues for internal work.
- Use clear public-facing language and navigation without assuming that visitors are specialists.

## Branding and existing ArcGIS Hub theme

The owner supplied these County colors:

| Color name | Hex value |
| --- | --- |
| Pinal blue | `#2f4a58` |
| Pinal teal | `#549898` |
| Pinal gold | `#d29040` |
| Pinal tan | `#d6cbaf` |

Existing variations include `#477f7f` for links and `#f1ede3` and `#fcfaf6` for row backgrounds. The owner welcomes variations and shades but wants a small, consistent palette with memorable names and documented purposes. The earlier contrast rationale for `#477f7f` is context, not a completed accessibility assessment; evaluate actual foreground/background combinations as pages are designed.

The supplied ArcGIS theme screenshot records:

| Theme setting | Current value |
| --- | --- |
| Global navigation background | `#2f4a58` |
| Global navigation text | `#fcfaf6` |
| Header background | `#fcfaf6` |
| Header text | `#2f4a58` |
| Body background | `#ffffff` |
| Body text | `#2f4a58` |
| Body links | `#477f7f` |
| Base font | Roboto |
| Heading font | Roboto Condensed |

These are the existing design reference, not a complete review of the current portal. The County accessibility reference supplied by the owner is recorded below.

## Accessibility reference and development requirements

The owner supplied [Pinal County's Accessibility page](https://www.pinal.gov/153/Accessibility), reviewed October 21, 2026. It states that the County works toward Section 508 and WCAG 2.0 Levels A and AA. It names JAWS, NVDA, VoiceOver, and keyboard-only navigation as supported technologies. This records the page's stated guidance; it is not a determination of all applicable legal obligations.

Use this reference throughout development, with the [W3C WCAG 2.0 specification](https://www.w3.org/TR/WCAG20/) for criteria details:

- Preserve meaningful headings, landmarks, descriptive links, and appropriate text alternatives. Decorative images and icons must not add redundant announcements.
- Make functions keyboard-operable, provide visible focus, and preserve a working skip link and logical focus order.
- Check actual text/background contrast: at least 4.5:1 for ordinary text and 3:1 for qualifying large text. Do not use color alone to convey meaning.
- Verify text resizing to 200% without losing content or functionality; relative units alone do not establish this.
- Review complete pages, including Tableau embeds and their information access, rather than treating accessible surrounding HTML as sufficient. Where a dashboard presents barriers, identify an appropriate accessible way to obtain equivalent information.
- Repeat relevant checks in ArcGIS Hub after text-card integration, including Hub's shared shell and inherited styles.

Current source includes headings and landmarks, a skip link, descriptive native links, focus styles, and decorative-image handling. Selected contrast pairs have been calculated. Manual keyboard, zoom, screen-reader, embed, and Hub checks remain pending; no full conformance claim has been made. Add the County accessibility link when implementing the footer.

### Supplied images

The owner added three images currently used on the site. They have been inspected locally and their filenames preserved:

- `images/SVG Hub - Gold 1.png`: gold Pinal County logo, identified by the owner as the "Hub" image. Despite its name, the supplied file is a PNG.
- `images/pinal-dotted-hero-banner-2400x800.png`: pale dotted banner background.
- `images/Pinal Map.png`: pale regional map with Pinal County outlined in gold.

## Existing portal and hierarchy

The links and content descriptions below were provided by the owner. A visual and content audit is still pending.

- [Portal homepage](https://economic-workforce-data-portal-pinal.hub.arcgis.com/)
  - [Economic Indicators](https://key-performance-indicators-pinal.hub.arcgis.com/): overview plus population, civilian labor force, unemployment, GDP, jobs, average earnings, and commuting patterns.
  - [ARIZONA@WORK Pinal County Performance](https://workforce-performance-pinal.hub.arcgis.com/)
    - [Federal Performance](https://federal-performance-measures-pinal.hub.arcgis.com/)
    - [Participants, Training & Outcomes / Activity and Outcomes](https://workforce-outcomes-pinal.hub.arcgis.com/)
  - Targeted Industries: currently an in-development section on the homepage.
  - [H3 Occupation Analysis](https://h3-occupation-analysis-pinal.hub.arcgis.com/)

Activity and Outcomes belongs beneath Workforce Performance, which belongs beneath the portal homepage. It is not a fifth main portal topic. Final page naming remains to be settled.

## Activity and Outcomes: confirmed needs

The owner finds the current page too long and overwhelming. Retain both perspectives:

- Current program activity.
- Mature participant outcomes.

## Proposals — not yet implemented or finalized

Create a shorter Activity and Outcomes overview with questions grouped under the two perspectives. Questions would link to supporting dashboard pages, potentially grouped as:

- Program participation and participation trends.
- Training activity and career fields.
- Current employment connections.
- Mature participant and training outcomes.

The exact questions, supporting page groupings, URLs, navigation labels, and layout remain proposals. The method for maintaining shared header and footer markup across multiple local pages remains to be established before adding a second page.

## First implementation increment

- The owner approved beginning with the homepage header and introduction, plus three separate style files.
- `index.html` contains this initial page increment, with no JavaScript, framework, or build tool.
- `css/components.css` holds reusable components, responsive layout rules, and keyboard focus styling.
- `css/pinal-theme.css` holds the named palette, purpose-based values, fonts, and introductory background image choice.
- `css/arcgis-compat.css` is reserved for verified Hub adjustments and currently contains comments only.
- The supplied logo and map image are used locally. The source homepage's introductory background references `Group 26 (2).png`; the supplied map is a local adaptation, not a verified match to that resource.
- The live homepage source was retrieved and decoded successfully. Its text-card HTML/CSS, header/footer, theme, and row configuration were inspected. Rendered appearance and Hub behavior have not yet been verified.
- Header navigation initially linked to local sections; the approved topic dropdown below replaces those links. About and the footer were added in the later homepage completion increment below.
- Shared CSS scopes to `.data-portal` to support later text-card preparation without styling unrelated Hub content.
- README documents preview steps, file responsibilities, palette names, and the current limits of shared markup maintenance.
- Source checks confirmed local asset paths, local anchors, CSS image paths, custom-property definitions, and one main page heading. The introductory label initially used blue over a translucent panel; the later typography refinement below supersedes that choice. Browser, keyboard, mobile, and Hub verification remain pending.

### Second increment: topic cards

- The owner previewed the header and introduction and reported that they look good. No separate mobile or keyboard result was reported.
- Added the four main topic cards using the existing homepage as the source reference, with larger labels, named theme values, and decorative inline SVG icons instead of a runtime icon dependency.
- Three cards link to the existing live topic pages. Targeted Industries remains visibly in development without a placeholder link.
- The Economic Indicators description matches the known indicator inventory, rather than carrying over unverified housing and business coverage from the source copy.
- Card layout uses four, two, or one column as viewport width decreases. Browser verification of the new section remains pending.

### Typography refinement requested by the owner

- Keep the hero eyebrow at 0.875rem; section eyebrows were initially reduced to 0.75rem, then to 0.6875rem at the owner's request, including the question dropdown eyebrow.
- Dark teal for eyebrows, card labels, and links was initially `#477f7f`. At the owner's request, the shared `pinal-teal-dark` value is now `#427777`, providing about 4.87:1 contrast on Pinal cream and 5.08:1 on white. This replaces the existing variation without adding another shade.
- Make the hero text panel solid white so its dark-teal eyebrow has consistent contrast over the map.
- Reduce card labels to 0.6875rem and card descriptions to 0.875rem. These correspond to 11px and 14px at the default 16px root size. Visual review of this refinement remains pending.

### Question section preview

- The owner found the existing question cards and nested question dropdowns too prominent and complex, and requested a preview of the recommended grouped text-link format.
- Added a question section beneath the topic cards, with four topic headings, direct question links, and a plain Targeted Industries development note.
- Layout uses two columns on desktop and one on narrow screens, with modest headings and underlined links on white. Following review, the owner requested keeping one outer dropdown around this simpler interior. It uses native `details`/`summary`, closed by default, with keyboard focus styling. No per-question dropdowns, answer descriptions, additional cards, or JavaScript are used.
- The owner requested the existing site's outer header style and wording: "Not sure where to begin?", the shortened heading "Start with the Question", and "Browse Questions" with a plus on the right. The header now uses blue, cream, and one named pale teal from the published source (`#b8dada`), with a plus that becomes a minus when expanded. The simplified white interior remains.
- The owner clarified that questions should describe information readers may be interested in; several questions may intentionally link to the same destination. Do not combine questions solely because their links match.
- Economic Indicators now includes four questions covering economic change, employment and unemployment, county and municipal population, and population projections. The owner confirmed that Economic Indicators contains projections.
- The owner requested adding the suggested questions for all topics. Economic Indicators, Workforce Performance, and H3 now each have four linked questions. Targeted Industries has three planned questions as non-linked text beneath its development note.
- Workforce questions link to the existing Federal Performance and Activity and Outcomes branches; Economic Indicators and H3 questions link to their respective overview/tools from the owner-provided portal map. Multiple questions may share these destinations.
- This is an implemented visual proposal for owner review, not final approval of the format or question wording. Supporting-page link refinement and browser/keyboard verification remain pending.

### About and footer increment

- The owner requested skipping the separate Targeted Industries section. The main topic card and planned questions continue to represent that portal topic.
- Added About and a shared footer pattern using the source homepage's wording and links. At the owner's request, About uses Pinal cream. Its eyebrow now uses the updated dark teal, which meets ordinary-text contrast on cream; the temporary blue override was removed.
- The footer uses the blue background, gold top border, and named light-teal accents. It includes Department Home, Accessibility, and a working local Back to top anchor.
- This is the first complete local homepage draft for review, excluding the skipped industry promotional section. Shared markup inclusion across multiple pages, GitHub publishing, mobile/keyboard/screen-reader verification, and Hub integration remain outstanding.

### Shared navigation refinement

- The owner approved replacing the three homepage section links with one "Explore topics" dropdown beside the linked logo and portal name.
- Native `details`/`summary` provides click and keyboard disclosure behavior without JavaScript. The dropdown starts closed, links to the three available live topic pages, and identifies Targeted Industries as in development without a link.
- On desktop the dropdown overlays the content below the toggle; at narrow widths it expands within the header. Visible focus and text contrast use existing theme values.
- Keep this header pattern across future pages, with breadcrumbs beneath it on interior pages. Automatic shared markup inclusion remains to be chosen before adding a second local page.
- Source checks can verify targets and markup; browser, keyboard, and screen-reader behavior still require manual review.

### Browser automation setup

- Python 3.14.8 is available locally. Installed Playwright 1.64.0 and its dependencies in the repository-local `.venv`, with reproducible versions in `requirements-dev.txt`.
- Added `tools/check_browser.py`, which launches installed Edge in an isolated headless session, serves the homepage temporarily on loopback, and checks 1280px and 390px viewports.
- Verified both dropdowns respond to keyboard activation, all 12 question links are exposed when expanded, HTML images load, and neither tested width has horizontal overflow. Captured screenshots and inspected the desktop question view and phone navigation view.
- `.venv/` and `.browser-checks/` are ignored by Git. The script closes its server and browser after running. Browser process launches required execution outside the sandbox; permission was approved and the check completed successfully.
- Script-driven browser testing is now established. This does not connect an interactive browser-control tool to the chat and is not a full accessibility audit. Zoom, comprehensive keyboard/focus, screen-reader, external-link, and Hub verification remain outstanding.

### Homepage verification and publication handoff

- The owner requested all available checks, then clarified that the assistant must pause afterward and walk the owner through committing, pushing, and GitHub Pages setup. Do not perform those Git/GitHub actions on the owner's behalf under the earlier instruction.
- Expanded automated verification is saved as `tools/verify_homepage.py`. Its final run completed 81 checks: 79 passed, no failures, and two County-domain links inconclusive due to Cloudflare blocking automated requests. README records the detailed scope and limits; raw evidence is ignored under `.browser-checks/`.
- Edge passed ten widths from 320px to 1920px, native 200% and 400% zoom, 200% root text-size stress tests, increased text spacing, keyboard order and focus checks, skip-link navigation, disclosure state exposure, local resources, and GitHub Pages project-subpath resource loading. Chrome passed the basic desktop and phone checks.
- axe-core 4.11.4 reported zero violations with dropdowns closed and expanded. Decorative arrow contrast items were reviewed against their inherited colors; all eight text/background combinations tested exceed 4.5:1. This is not a full conformance claim.
- Five distinct ArcGIS destinations returned HTTP 200 with expected page content. The County Department Home link redirected to `/1849/Economic-Workforce-Development`, and the footer was updated to that current URL. The County Department Home and Accessibility pages were independently readable through the web reader, despite blocking automated direct/browser checks.
- Screen-reader listening tests are skipped at the owner's request. Safari/Firefox and Hub integration remain untested. Deployment verification must follow the owner's eventual GitHub Pages setup.
- No commits, pushes, or GitHub Pages configuration changes were performed.

## Setup confirmed on October 21, 2026

- Git is installed locally.
- VS Code is installed and its command is available.
- The GitHub repository exists and contains a README.
- The repository was successfully cloned into `C:\Users\laural\Documents\Website Projects\pinal-data-portal`.
- Local branch `main` tracks `origin/main`.
- The remote is `https://github.com/lloiaco/pinal-data-portal.git`.
- Codex can inspect this local checkout and create project files.
- GitHub CLI is not installed; it is optional for the initial workflow.
- Authenticated push access and GitHub Pages settings have not been verified.
- The first local homepage increment has been added. No framework, build tool, or deployment configuration has been introduced.

## Next steps

1. Open the cloned repository folder in VS Code and verify the local editing workflow.
2. Commit and push this brief, verifying write access to GitHub.
3. Review the existing portal design and record reusable visual patterns.
4. Establish a small project structure and shared design approach.
5. Develop the homepage and Activity and Outcomes branch in focused increments.
6. Configure and verify GitHub Pages when there is a first page ready to preview.
7. At the owner's request, prepare completed pages as ArcGIS Hub text-card sections and verify them in Hub before work publication.
