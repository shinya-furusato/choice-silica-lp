from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
text = (SRC / "main.html").read_text(encoding="utf-8")
for n in range(1, 21):
    section = (SRC / "sections" / f"section-{n:02d}.html").read_text(encoding="utf-8")
    text = text.replace(f"{{{{SECTION_{n:02d}}}}}", section)

# The final CTA artwork starts at the bottom of section 15 and continues
# through sections 16-17. Extend section 15 by the same 2px used there
# to prevent a subpixel white seam at the upper-right edge.
cta_seam_patch = """
<style id="cta-seam-fix-section15">
[data-section-id="page-1-section-15"] > .lp-visual-layer {
  left: 0 !important;
  right: auto !important;
  width: calc(100% + 2px) !important;
}
</style>
"""
text = text.replace("</head>", cta_seam_patch + "\n</head>", 1)

(ROOT / "index.html").write_text(text, encoding="utf-8")
print(f"Built {ROOT / 'index.html'}")
