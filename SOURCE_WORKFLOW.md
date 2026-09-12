# Choice Silica LP source workflow

`index.html` remains the ecforce-ready, single-file deliverable.

Edit these source files instead of editing the generated 4 MB file directly:

- `src/main.html`: document shell, metadata, and placeholders
- `src/styles.css`: normal inline CSS
- `src/fonts.css`: embedded font data
- `src/sections/section-XX.html`: one LP section per file
- `build/build.py`: rebuilds the final `index.html`

When a source file is pushed to `main`, GitHub Actions rebuilds and commits `index.html`.
