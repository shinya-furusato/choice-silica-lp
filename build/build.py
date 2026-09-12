from pathlib import Path
import html as html_lib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
SECTIONS = SRC / "sections"
AI_MAP_PATH = SRC / "ai-map.json"
AI_TEXT_MAP_PATH = SRC / "ai-text-map.json"

html = (SRC / "main.html").read_text(encoding="utf-8")
html = html.replace("{{FONTS_CSS}}", (SRC / "fonts.css").read_text(encoding="utf-8"))
html = html.replace("{{STYLES_CSS}}", (SRC / "styles.css").read_text(encoding="utf-8"))

ai_sections = {}
if AI_MAP_PATH.exists():
    ai_map = json.loads(AI_MAP_PATH.read_text(encoding="utf-8"))
    ai_sections = ai_map.get("sections", {})

ai_text_anchors = {}
if AI_TEXT_MAP_PATH.exists():
    ai_text_map = json.loads(AI_TEXT_MAP_PATH.read_text(encoding="utf-8"))
    ai_text_anchors = ai_text_map.get("anchors", {})


def add_attr(tag: str, name: str, value: str) -> str:
    if re.search(rf"\s{re.escape(name)}=", tag):
        return tag
    escaped = html_lib.escape(str(value), quote=True)
    return tag[:-1] + f' {name}="{escaped}">'


def inject_text_anchor(section_html: str, anchor_name: str, anchor: dict) -> str:
    phrase = anchor.get("text_contains")
    if not phrase:
        return section_html

    # Label direct text-bearing elements only. This keeps the Illustrator/PDF
    # geometry untouched while giving paired SVG/selectable text stable names.
    tag_pattern = re.compile(
        r"<(?P<tag>text|tspan|span|h[1-6]|p|div)\b(?P<attrs>[^>]*)>(?P<body>[^<]*"
        + re.escape(phrase)
        + r"[^<]*)",
        re.IGNORECASE,
    )

    def label(match):
        opening = f'<{match.group("tag")}{match.group("attrs")}>'
        opening = add_attr(opening, "data-ai-name", anchor_name)
        opening = add_attr(opening, "data-ai-role", anchor.get("type", "text-anchor"))
        opening = add_attr(opening, "data-ai-edit-policy", anchor.get("edit_policy", "paired-text-edit"))
        return opening + match.group("body")

    return tag_pattern.sub(label, section_html)


def inject_link_anchor(section_html: str, anchor_name: str, anchor: dict) -> str:
    selector = anchor.get("selector", "")
    m = re.fullmatch(r"\[data-ai-name=['\"]([^'\"]+)['\"]\]", selector)
    if not m:
        return section_html
    generated_name = m.group(1)

    pattern = re.compile(r"<a\b[^>]*\bdata-ai-name=[\"']" + re.escape(generated_name) + r"[\"'][^>]*>")

    def label(match):
        tag = match.group(0)
        tag = add_attr(tag, "data-ai-anchor", anchor_name)
        tag = add_attr(tag, "data-ai-edit-policy", anchor.get("edit_policy", "safe-attribute-edit"))
        return tag

    return pattern.sub(label, section_html)


def inject_ai_metadata(section_html: str, filename: str) -> str:
    meta = ai_sections.get(filename)
    if not meta:
        return section_html

    section_match = re.search(r"<section\b[^>]*>", section_html)
    if not section_match:
        return section_html

    section_tag = section_match.group(0)
    section_tag = add_attr(section_tag, "data-ai-section", filename.removesuffix(".html"))
    section_tag = add_attr(section_tag, "data-ai-name", meta.get("ai_name", filename.removesuffix(".html")))
    section_tag = add_attr(section_tag, "data-ai-role", meta.get("ai_role", "content"))
    section_html = section_html[:section_match.start()] + section_tag + section_html[section_match.end():]

    # Mark the first semantic heading in every section without changing layout or styling.
    heading_match = re.search(r"<h([1-6])\b[^>]*>", section_html)
    if heading_match:
        heading_tag = add_attr(heading_match.group(0), "data-ai-role", "section-heading")
        section_html = section_html[:heading_match.start()] + heading_tag + section_html[heading_match.end():]

    # CTA sections receive stable link labels so purchase/navigation targets are easy for AI to locate.
    if meta.get("ai_role") == "cta":
        link_index = 0

        def label_link(match):
            nonlocal link_index
            link_index += 1
            tag = match.group(0)
            tag = add_attr(tag, "data-ai-role", "cta-link")
            tag = add_attr(tag, "data-ai-name", f'{meta.get("ai_name", filename.removesuffix(".html"))}-link-{link_index}')
            return tag

        section_html = re.sub(r"<a\b[^>]*>", label_link, section_html)

    # Third-layer semantic anchors are injected only when the anchor belongs to
    # this resolved section. Text anchors may appear twice by design (rendered
    # SVG text + selectable text); both receive the same stable semantic name.
    section_ai_name = meta.get("ai_name")
    for anchor_name, anchor in ai_text_anchors.items():
        if anchor.get("section") != section_ai_name:
            continue
        if anchor.get("type") == "link":
            section_html = inject_link_anchor(section_html, anchor_name, anchor)
        else:
            section_html = inject_text_anchor(section_html, anchor_name, anchor)

    return section_html


section_files = sorted(SECTIONS.glob("section-*.html"))
if not section_files:
    raise RuntimeError("No section source files found.")

for i, section_file in enumerate(section_files, 1):
    token = f"{{{{SECTION_{i:02d}}}}}"
    if token not in html:
        raise RuntimeError(f"Missing placeholder: {token}")
    section_html = section_file.read_text(encoding="utf-8")
    section_html = inject_ai_metadata(section_html, section_file.name)
    html = html.replace(token, section_html, 1)

if "{{FONTS_CSS}}" in html or "{{STYLES_CSS}}" in html or re.search(r"\{\{SECTION_\d+\}\}", html):
    raise RuntimeError("Unresolved build placeholders remain.")

(ROOT / "index.html").write_text(html, encoding="utf-8", newline="")
print(f"Built index.html ({len(html.encode('utf-8')):,} bytes)")
