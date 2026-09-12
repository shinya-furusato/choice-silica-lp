from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
SECTIONS = SRC / "sections"

html = (SRC / "main.html").read_text(encoding="utf-8")
html = html.replace("{{FONTS_CSS}}", (SRC / "fonts.css").read_text(encoding="utf-8"))
html = html.replace("{{STYLES_CSS}}", (SRC / "styles.css").read_text(encoding="utf-8"))

section_files = sorted(SECTIONS.glob("section-*.html"))
if not section_files:
    raise RuntimeError("No section source files found.")

for i, section_file in enumerate(section_files, 1):
    token = f"{{{{SECTION_{i:02d}}}}}"
    if token not in html:
        raise RuntimeError(f"Missing placeholder: {token}")
    html = html.replace(token, section_file.read_text(encoding="utf-8"), 1)

if "{{FONTS_CSS}}" in html or "{{STYLES_CSS}}" in html or re.search(r"\{\{SECTION_\d+\}\}", html):
    raise RuntimeError("Unresolved build placeholders remain.")

(ROOT / "index.html").write_text(html, encoding="utf-8", newline="")
print(f"Built index.html ({len(html.encode('utf-8')):,} bytes)")
