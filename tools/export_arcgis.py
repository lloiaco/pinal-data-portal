"""Prepare paste-ready Hub fragments from the maintained HTML and CSS.

Uses Python's standard library only. This exports copies; it is not required
to preview, run, or deploy the standalone website.
"""

import json
import re
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "arcgis" / "homepage"
HOME = "https://economic-workforce-data-portal-pinal.hub.arcgis.com/"
RESOURCE = "https://www.arcgis.com/sharing/rest/content/items/cfeb05c86b994a0b829fb8614b93936c/resources/"
LOGO = RESOURCE + "SVG%20Hub%20-%20Gold%201.png"
MAP = RESOURCE + "Group%2026%20%282%29.png"
PARTS = (
    ("01-header", "header", "class", "site-header", "header", "#2f4a58"),
    ("02-introduction", "section", "id", "explore-data", "intro", "#fcfaf6"),
    ("03-topic-cards", "section", "id", "topics", "topics", "#ffffff"),
    ("04-questions", "section", "id", "find-answers", "questions", "#2f4a58"),
    ("05-about", "section", "id", "about", "about", "#fcfaf6"),
    ("06-footer", "footer", "class", "site-footer", "footer", "#2f4a58"),
)


def extract_element(html, tag, attribute, value):
    pattern = re.compile(rf'<{tag}\b[^>]*\b{attribute}="{re.escape(value)}"[^>]*>')
    start = pattern.search(html)
    if not start:
        raise ValueError(f"Missing source element: {tag} {attribute}={value}")
    depth = 0
    for match in re.finditer(rf"</?{tag}\b[^>]*>", html[start.start():]):
        depth += -1 if match.group().startswith("</") else 1
        if depth == 0:
            return dedent(html[start.start():start.start() + match.end()]).strip()
    raise ValueError(f"Unclosed source element: {value}")


def css_blocks(css):
    """Read the balanced rule blocks used by our small, buildless stylesheets."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    position = 0
    while position < len(css):
        opening = css.find("{", position)
        if opening == -1:
            if css[position:].strip():
                raise ValueError("Unsupported CSS outside a rule")
            break
        depth = 1
        end = opening + 1
        quote = None
        while depth and end < len(css):
            char = css[end]
            if quote:
                if char == quote and css[end - 1] != "\\":
                    quote = None
            elif char in ("'", '"'):
                quote = char
            elif char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
            end += 1
        if depth:
            raise ValueError("Unbalanced CSS block")
        yield css[position:opening].strip(), css[opening + 1:end - 1].strip()
        position = end


def select_css(css, classes):
    output = []
    for selector, body in css_blocks(css):
        if selector.startswith("@media"):
            nested = select_css(body, classes)
            if nested:
                output.append(f"{selector} {{\n{nested}\n}}")
        elif selector.startswith("@"):
            raise ValueError(f"Unsupported export CSS directive: {selector}")
        else:
            matches = [part.strip() for part in selector.split(",")
                       if set(re.findall(r"\.([a-zA-Z_][\w-]*)", part)).issubset(classes)]
            if matches:
                output.append(",\n".join(matches) + " {\n  " + body.replace("\n", "\n  ") + "\n}")
    return "\n\n".join(output)


def compatible_colors(css):
    # Use conventional rgba() syntax in Hub's custom CSS/Sass editors.
    return re.sub(r"rgb\((\d+)\s+(\d+)\s+(\d+)\s*/\s*([\d.]+)%\)",
                  lambda m: f"rgba({m[1]}, {m[2]}, {m[3]}, {float(m[4]) / 100:g})", css)


def write(name, content):
    (OUTPUT / name).write_text(content.rstrip() + "\n", encoding="utf-8")


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    theme = (ROOT / "css/pinal-theme.css").read_text(encoding="utf-8")
    theme = theme.replace('../images/Pinal%20Map.png', MAP)
    components = (ROOT / "css/components.css").read_text(encoding="utf-8")
    compatibility = (ROOT / "css/arcgis-compat.css").read_text(encoding="utf-8")
    previews = []
    shell_styles = []
    manifest = {"home_url": HOME, "logo_url": LOGO, "row_map_url": MAP, "sections": []}
    for filename, tag, attribute, value, suffix, background in PARTS:
        fragment = extract_element(html, tag, attribute, value)
        fragment = fragment.replace('href="index.html"', f'href="{HOME}"')
        fragment = fragment.replace('src="images/SVG%20Hub%20-%20Gold%201.png"', f'src="{LOGO}"')
        # Hub's header can be fixed, so an anchor inside it cannot scroll the page.
        # An empty fragment goes to the current document's top without a new ID.
        fragment = fragment.replace('href="#top"', 'href="#"')
        if suffix == "topics":
            icons = iter(("graph-time-series", "group", "organization", "investigation"))
            fragment = re.sub(r"<svg\b.*?</svg>", lambda _: (
                '<span class="topic-card__icon" aria-hidden="true">'
                f'<calcite-icon icon="{next(icons)}" scale="l"></calcite-icon></span>'
            ), fragment, flags=re.S)
        wrapper = f"data-portal hub-portal--{suffix}"
        fragment = f'<div class="{wrapper}">\n{fragment}\n</div>'
        classes = set(" ".join(re.findall(r'class="([^"]+)"', fragment)).split())
        css = select_css(theme + "\n" + components, classes)
        css = css.replace(".data-portal", f".data-portal.hub-portal--{suffix}")
        css += "\n\n" + select_css(compatibility, classes)
        css = compatible_colors(css)
        notice = f"Generated from index.html and css/ by tools/export_arcgis.py. Regenerate after source edits."
        if suffix in ("header", "footer"):
            write(filename + ".html", f"<!-- {notice} Paste into Hub custom {suffix} HTML. -->\n" + fragment)
            write(filename + ".css", f"/* {notice} Paste into Hub custom {suffix} CSS, without style tags. */\n" + css)
            previews.append(fragment)
            shell_styles.append(css)
        else:
            output = f"<!-- {notice} Paste this whole file into ONE Text card's HTML editor. -->\n<style>\n{css}\n</style>\n{fragment}"
            write(filename + ".html", output)
            row_style = f"background-color:{background};"
            if suffix == "intro":
                row_style += f"background-image:url('{MAP}');background-position:center;background-size:cover;"
            previews.append(f'<div style="{row_style}">{output}</div>')
        manifest["sections"].append({"file": filename + ".html", "suffix": suffix,
                                     "row_background": background,
                                     "css_file": filename + ".css" if suffix in ("header", "footer") else None})
    preview = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ArcGIS homepage sections — local assembly preview</title>
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;600;700&amp;family=Roboto+Condensed:wght@500;600;700&amp;display=swap" rel="stylesheet">
<script type="module" src="https://hubcdn.arcgis.com/opendata-ui/assets/calcite-components/5.1.1/cdn/index.js"></script>
<style>body {{margin:0;}}\n{"\n".join(shell_styles)}</style>
</head>
<body>
<!-- Preview only: this models row backgrounds, not Hub's editor or sanitizer. -->
{previews[0]}
<main>{"\n".join(previews[1:-1])}</main>
{previews[-1]}
</body>
</html>'''
    write("preview.html", preview)
    write("manifest.json", json.dumps(manifest, indent=2))
    print("Exported six homepage sections, separate header/footer CSS, and a local assembly preview.")


if __name__ == "__main__":
    main()
