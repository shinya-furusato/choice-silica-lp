from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
text = (SRC / "main.html").read_text(encoding="utf-8")
for n in range(1, 21):
    section = (SRC / "sections" / f"section-{n:02d}.html").read_text(encoding="utf-8")
    text = text.replace(f"{{{{SECTION_{n:02d}}}}}", section)
(ROOT / "index.html").write_text(text, encoding="utf-8")
print(f"Built {ROOT / 'index.html'}")
