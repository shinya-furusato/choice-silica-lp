from pathlib import Path
import re, hashlib

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
SRC = ROOT / "src"
SECTIONS = SRC / "sections"
BUILD = ROOT / "build"
WORKFLOWS = ROOT / ".github" / "workflows"

original_bytes = INDEX.read_bytes()
html = original_bytes.decode("utf-8")

style_matches = list(re.finditer(r"<style(?:\s[^>]*)?>(.*?)</style>", html, flags=re.S | re.I))
font_match = next((m for m in style_matches if "@font-face" in m.group(1)), None)
if font_match is None:
    raise RuntimeError("Could not find inline font style block.")
other_style_matches = [m for m in style_matches if m is not font_match]
if len(other_style_matches) != 1:
    raise RuntimeError(f"Expected exactly one non-font style block, found {len(other_style_matches)}.")
styles_match = other_style_matches[0]

section_matches = list(re.finditer(r"<section\b.*?</section>", html, flags=re.S | re.I))
if not section_matches:
    raise RuntimeError("No LP sections found.")

SECTIONS.mkdir(parents=True, exist_ok=True)
BUILD.mkdir(parents=True, exist_ok=True)
WORKFLOWS.mkdir(parents=True, exist_ok=True)

replacements = [
    (font_match.start(1), font_match.end(1), "{{FONTS_CSS}}"),
    (styles_match.start(1), styles_match.end(1), "{{STYLES_CSS}}"),
]

for i, match in enumerate(section_matches, 1):
    replacements.append((match.start(), match.end(), f"{{{{SECTION_{i:02d}}}}}"))
    (SECTIONS / f"section-{i:02d}.html").write_text(match.group(0), encoding="utf-8", newline="")

template = html
for start, end, replacement in sorted(replacements, reverse=True):
    template = template[:start] + replacement + template[end:]

(SRC / "main.html").write_text(template, encoding="utf-8", newline="")
(SRC / "fonts.css").write_text(font_match.group(1), encoding="utf-8", newline="")
(SRC / "styles.css").write_text(styles_match.group(1), encoding="utf-8", newline="")

build_script = '''from pathlib import Path
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
'''
(BUILD / "build.py").write_text(build_script, encoding="utf-8", newline="")

build_workflow = '''name: Build ecforce index.html

on:
  push:
    branches: [main]
    paths:
      - "src/**"
      - "build/build.py"
  workflow_dispatch:

permissions:
  contents: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Build index.html
        run: python build/build.py
      - name: Commit generated index.html
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add index.html
          if git diff --cached --quiet; then
            echo "index.html is already up to date."
          else
            git commit -m "Build index.html from editable sources"
            git push
          fi
'''
(WORKFLOWS / "build-index.yml").write_text(build_workflow, encoding="utf-8", newline="")

guide = '''# Choice Silica LP source workflow

`index.html` remains the ecforce-ready, single-file deliverable.

Edit these source files instead of editing the generated 4 MB file directly:

- `src/main.html`: document shell, metadata, and placeholders
- `src/styles.css`: normal inline CSS
- `src/fonts.css`: embedded font data
- `src/sections/section-XX.html`: one LP section per file
- `build/build.py`: rebuilds the final `index.html`

When a source file is pushed to `main`, GitHub Actions rebuilds and commits `index.html`.
'''
(ROOT / "SOURCE_WORKFLOW.md").write_text(guide, encoding="utf-8", newline="")

exec(compile(build_script, str(BUILD / "build.py"), "exec"), {"__name__":"__main__"})
rebuilt_bytes = INDEX.read_bytes()
if rebuilt_bytes != original_bytes:
    raise RuntimeError(
        "Rebuilt index.html is not byte-for-byte identical to the original. "
        f"original={hashlib.sha256(original_bytes).hexdigest()} "
        f"rebuilt={hashlib.sha256(rebuilt_bytes).hexdigest()}"
    )

print(f"Initialized {len(section_matches)} editable sections.")
print(f"SHA-256 verified: {hashlib.sha256(original_bytes).hexdigest()}")
