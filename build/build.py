from pathlib import Path
import re

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

# Q&A 3rd answer: keep the approved wording concise while preserving
# the existing PDF-derived typography and placement.
qa3_answer = """<h2 id="lp-heading-page-1-native-166" class="lp-text lp-text--heading lp-text--pdf-svg" style="z-index:8946;" data-source="native" data-confidence="1.00" data-paint-order="8944" data-pdf-baseline="true"><svg class="lp-native-text-svg" viewBox="0 11168 299.671 568" preserveAspectRatio="none" aria-hidden="true" focusable="false"><text x="51.59450759999999" y="11545.960935399999" textLength="219.98875600000008" lengthAdjust="spacingAndGlyphs" fill="#000009" stroke="none" stroke-width="0" opacity="1.000" style="font-family:'g_d1_f4','Noto Sans JP','Yu Gothic','Hiragino Kaku Gothic ProN',sans-serif;font-size:12.0357px;font-weight:400;font-style:normal;letter-spacing:0.04px;word-spacing:-0.04px;mix-blend-mode:normal;paint-order:stroke fill" transform="translate(51.59450759999999 11545.960935399999) matrix(0.9784806866239604 0 0 1 0 0) translate(-51.59450759999999 -11545.960935399999)">これから新しい商品も発売しますので、</text></svg><span class="lp-selection-text" style="left:17.2171%;top:64.0844%;width:73.4101%;min-height:3.0683%;font-size:clamp(1px,4.0163cqw,24px);font-weight:400;font-family:'g_d1_f4','Noto Sans JP','Yu Gothic','Hiragino Kaku Gothic ProN',sans-serif;font-style:normal;text-align:left;line-height:1.1800;letter-spacing:0.0133cqw;word-spacing:-0.0133cqw;transform-origin:0 0;transform:matrix(0.97848,0,0,1,0,0);direction:ltr">これから新しい商品も発売しますので、</span></h2>
<h2 id="lp-heading-page-1-native-167" class="lp-text lp-text--heading lp-text--pdf-svg" style="z-index:8948;" data-source="native" data-confidence="1.00" data-paint-order="8946" data-pdf-baseline="true"><svg class="lp-native-text-svg" viewBox="0 11168 299.671 568" preserveAspectRatio="none" aria-hidden="true" focusable="false"><text x="51.59450759999999" y="11563.508985999999" textLength="195.4932200000001" lengthAdjust="spacingAndGlyphs" fill="#000009" stroke="none" stroke-width="0" opacity="1.000" style="font-family:'g_d1_f4','Noto Sans JP','Yu Gothic','Hiragino Kaku Gothic ProN',sans-serif;font-size:12.0357px;font-weight:400;font-style:normal;letter-spacing:0.04px;word-spacing:-0.04px;mix-blend-mode:normal;paint-order:stroke fill" transform="translate(51.59450759999999 11563.508985999999) matrix(0.9784806866239604 0 0 1 0 0) translate(-51.59450759999999 -11563.508985999999)">積あがっていけば、支援に繋がり、</text></svg><span class="lp-selection-text" style="left:17.2171%;top:67.1739%;width:65.2359%;min-height:3.0683%;font-size:clamp(1px,4.0163cqw,24px);font-weight:400;font-family:'g_d1_f4','Noto Sans JP','Yu Gothic','Hiragino Kaku Gothic ProN',sans-serif;font-style:normal;text-align:left;line-height:1.1800;letter-spacing:0.0133cqw;word-spacing:-0.0133cqw;transform-origin:0 0;transform:matrix(0.97848,0,0,1,0,0);direction:ltr">積あがっていけば、支援に繋がり、</span></h2>
<h2 id="lp-heading-page-1-native-168" class="lp-text lp-text--heading lp-text--pdf-svg" style="z-index:8950;" data-source="native" data-confidence="1.00" data-paint-order="8948" data-pdf-baseline="true"><svg class="lp-native-text-svg" viewBox="0 11168 299.671 568" preserveAspectRatio="none" aria-hidden="true" focusable="false"><text x="51.59450759999999" y="11581.0570366" textLength="183.12768500000006" lengthAdjust="spacingAndGlyphs" fill="#000009" stroke="none" stroke-width="0" opacity="1.000" style="font-family:'g_d1_f4','Noto Sans JP','Yu Gothic','Hiragino Kaku Gothic ProN',sans-serif;font-size:12.0357px;font-weight:400;font-style:normal;letter-spacing:0.04px;word-spacing:-0.04px;mix-blend-mode:normal;paint-order:stroke fill" transform="translate(51.59450759999999 11581.0570366) matrix(0.9784806866239604 0 0 1 0 0) translate(-51.59450759999999 -11581.0570366)">現場がかわっていくと思います。</text></svg><span class="lp-selection-text" style="left:17.2171%;top:70.2633%;width:61.0956%;min-height:3.0683%;font-size:clamp(1px,4.0163cqw,24px);font-weight:400;font-family:'g_d1_f4','Noto Sans JP','Yu Gothic','Hiragino Kaku Gothic ProN',sans-serif;font-style:normal;text-align:left;line-height:1.1800;letter-spacing:0.0133cqw;word-spacing:-0.0133cqw;transform-origin:0 0;transform:matrix(0.97848,0,0,1,0,0);direction:ltr">現場がかわっていくと思います。</span></h2>"""

qa3_pattern = re.compile(
    r'<h2 id="lp-heading-page-1-native-166".*?</h2>\s*'
    r'<h2 id="lp-heading-page-1-native-167".*?</h2>\s*'
    r'<h2 id="lp-heading-page-1-native-168".*?</h2>\s*'
    r'<h2 id="lp-heading-page-1-native-169".*?</h2>\s*'
    r'<h2 id="lp-heading-page-1-native-170".*?</h2>\s*'
    r'<h2 id="lp-heading-page-1-native-171".*?</h2>',
    re.S,
)
text, count = qa3_pattern.subn(qa3_answer, text, count=1)
if count != 1:
    raise RuntimeError("Q&A third answer block was not found exactly once")

(ROOT / "index.html").write_text(text, encoding="utf-8")
print(f"Built {ROOT / 'index.html'}")
