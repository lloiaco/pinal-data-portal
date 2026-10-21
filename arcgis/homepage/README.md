# Homepage sections for ArcGIS Hub

These are paste-ready copies of the reviewed homepage. The maintained source remains `index.html`, `css/components.css`, and `css/pinal-theme.css`; integration rules remain in `css/arcgis-compat.css`.

Start with the custom header, then move through the four text-card rows and footer. You can apply and preview each part before continuing. This package does not save or publish anything to Hub.

## Files and destinations

| Order | File | Paste destination |
| --- | --- | --- |
| 1 | [01-header.html](01-header.html) and [01-header.css](01-header.css) | Header → Custom HTML/CSS → the separate HTML and CSS editors. |
| 2 | [02-introduction.html](02-introduction.html) | One full-width Text card, edited in HTML mode. |
| 3 | [03-topic-cards.html](03-topic-cards.html) | One full-width Text card. Keep all four topics together in this card. |
| 4 | [04-questions.html](04-questions.html) | One full-width Text card containing the entire outer dropdown. |
| 5 | [05-about.html](05-about.html) | One full-width Text card. |
| 6 | [06-footer.html](06-footer.html) and [06-footer.css](06-footer.css) | Footer → Custom → the separate HTML and CSS editors. |

For each Text card, copy the **whole file**, including its single `<style>` block and `.data-portal` wrapper. For header/footer CSS, paste raw CSS without adding `<style>` tags. Avoid combining the text-card files into one card: each file contains its own style block. The generated classes keep each section's styles scoped.

[preview.html](preview.html) assembles the fragments for browser review. Open it from File Explorer as with the standalone homepage. **Do not paste that preview document into Hub.** `manifest.json` is a reference for the file order, colors, and assets; it is not a Hub import file.

## 1. Header

In the site's layout editor, open **Customize → Header** and choose **Custom HTML/CSS**. Replace its HTML with `01-header.html` and its CSS with `01-header.css`. Use **Wide** for the header layout. Apply and preview.

The logo and portal name link to the ArcGIS portal homepage. The dropdown links to the three existing topic sites; Targeted Industries remains non-linked. The CSS includes a scoped correction for Hub's cream navigation background so the white header text stays readable on blue. Cream is used for backgrounds, not text.

Hub owns the surrounding main landmark and its skip-navigation controls. The standalone document's `<body>`, `<main>`, and skip link are not copied into these fragments. Check Hub's own skip link when reviewing the assembled page.

The custom header and footer apply to pages attached to **this Hub site**. Economic Indicators, Workforce Performance, and H3 are separate Hub sites; changing this homepage's settings does not update those sites. We will prepare those when developing their branches.

## 2. Four content rows

Use four rows in the order below. Each should contain **one Text card spanning the full row (12 columns)**. Use the row's **Wide** layout so the background can span the page; the code limits the content width internally. Remove the old hero's spacer columns/cards and the old versions of these sections so there are no duplicated headings or anchors. Skip the separate Targeted Industries promotional row.

| Text-card file | Hub row background | Hub row background image |
| --- | --- | --- |
| `02-introduction.html` | Pinal cream `#fcfaf6` | The verified map URL below; center it, without a tint/overlay or extra transparency. |
| `03-topic-cards.html` | White `#ffffff` | None. |
| `04-questions.html` | Pinal blue `#2f4a58` | None. |
| `05-about.html` | Pinal cream `#fcfaf6` | None. |

The code provides section spacing. Start without extra row spacing or spacer cards; if the editor offers padding controls, avoid adding padding on top of the code's spacing. If content is too narrow, check the row layout and Text card width before changing the CSS.

For the introductory Row's **Background image → Image URL**, use:

```text
https://www.arcgis.com/sharing/rest/content/items/cfeb05c86b994a0b829fb8614b93936c/resources/Group%2026%20%282%29.png
```

The exported introduction is transparent so the **Hub row** provides the map, while the text panel remains solid white. Without that row image setting, it will show the cream background. This is intentional.

For each Text card, use **Edit in HTML**, replace the old card content, then apply. Review the result before moving to the next row. Use HTML mode for future replacements so the rich-text toolbar does not restructure the markup.

## 3. Footer and theme

Choose **Customize → Footer → Custom**. Paste `06-footer.html` into HTML and `06-footer.css` into CSS. The Back to top link uses `href="#"`, which works with Hub's fixed header and does not depend on the standalone page's body ID.

Keep the following theme values consistent with the exports:

| Hub theme setting | Value |
| --- | --- |
| Global navigation background / text | `#2f4a58` / `#ffffff` |
| Header background / text | `#2f4a58` / `#ffffff` |
| Body background / text | `#ffffff` / `#2f4a58` |
| Body link | Updated dark teal `#427777` |
| Base font | Roboto |
| Heading font | Roboto Condensed |

Font import URLs, if needed:

```text
https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;600;700&display=swap
https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@500;600;700&display=swap
```

Hub's native global navigation, action bar, privacy controls, and platform footer are managed by Hub. This package does not replace them.

## Assets and compatibility

The map and logo URLs use the existing public ArcGIS homepage item's resources. Their SHA-256 hashes were compared with the local images and matched exactly. There is no GitHub Pages dependency for the fragments' images or CSS. Keep those ArcGIS resources publicly accessible.

The four inline SVG icons in the standalone topic cards are replaced with Hub-supported Calcite icons. The labels, questions, typography, colors, and responsive layouts come from the maintained source. There are no scripts in the paste files; the dropdowns use native HTML and Calcite icons use Hub's own runtime.

Prepared against [Esri's customization guidance](https://doc.esri.com/en/arcgis-hub/latest/build/customize-html-css.html), [text-card HTML and component support](https://doc.esri.com/en/arcgis-hub/latest/build/add-text-and-images.html), and [header/footer and theme instructions](https://doc.esri.com/en/arcgis-hub/latest/build/brand-site.html). Esri scans custom HTML; its guidance identifies `ADDSTYLE` as a possible sign of sanitization and advises consolidating styles when multiple style blocks cause problems.

## Verification and remaining Hub check

Passed fragment checks and browser assembly previews at 320, 390, 768, and 1280px, including icon loading and dropdowns. The exported sections were also inserted **only into an isolated browser's in-memory copy** of the current public Hub page. That confirmed key sizes/colors, desktop dropdown visibility, phone layout, the navigation background correction, and Back to top. No ArcGIS save or publish occurred.

This cannot test what Hub's editor preserves after paste. In the actual editor and saved preview, check:

- One introductory heading, all four cards, all questions, and the cream About row.
- The map and logo load, and all four Calcite icons appear.
- Both dropdowns start closed, open with click/Enter/Space, and retain visible keyboard focus.
- The header menu is visible above the next row, including with Hub's fixed header.
- IDs, `aria-label`, `aria-labelledby`, and decorative `aria-hidden` attributes survive; anchors and Back to top work.
- Narrow layout and 200% zoom have no clipped content or horizontal scrolling.
- Hub's own skip link and any attached-page navigation remain usable.

If the editor removes or changes markup, compare its saved HTML with the corresponding export before publishing. Screen-reader announcements remain untested, as agreed. These checks do not establish full accessibility conformance.

## Regenerating after source changes

From the repository's Bash terminal:

```bash
py tools/export_arcgis.py
```

The exporter uses Python's standard library; it does not require Playwright or a website build step. It overwrites the generated fragments, CSS, preview, and manifest while leaving this guide intact. Edit maintained source files rather than the generated copies. To rerun browser checks:

```bash
./.venv/Scripts/python.exe tools/check_arcgis_export.py
```

The check needs internet access and installed Edge. Test screenshots and results are saved under ignored `.browser-checks/`.
