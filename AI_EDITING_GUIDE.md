# AI Editing Guide

This repository is organized so that future LP revisions can be made safely from editable source files instead of editing the generated `index.html` directly.

## Source of truth

- `src/main.html`: page shell and section placeholders
- `src/sections/section-01.html` ... `section-20.html`: editable section sources
- `src/styles.css`: shared visual and interaction adjustments
- `src/fonts.css`: embedded font data
- `src/ai-map.json`: section-level semantic map
- `src/ai-elements.json`: editable/protected element policy
- `src/ai-text-map.json`: semantic anchors for text and CTA edits
- `build/build.py`: regenerates `index.html`

## Editing rules

1. Prefer text, URL, or image-reference edits before CSS/SVG changes.
2. Preserve SVG geometry (`path`, `clipPath`, `transform`, coordinates, `viewBox`) unless a layout correction explicitly requires it.
3. If visible SVG text has a paired selectable text layer, update both.
4. For CTA URL changes, edit the link target only unless copy/design changes are also requested.
5. For image swaps, change the referenced asset path without altering geometry when possible.
6. Scientific, health, and numeric claims require approved source material before changing.
7. Do not edit generated `index.html` as the long-term source. Rebuild it from `src/` with `python build/build.py`.

## Current approved visual fixes

- Paw cursor is used on clickable links/buttons.
- CTA right-edge white seam correction is included in the approved source.
- Current structure contains 20 sections.
