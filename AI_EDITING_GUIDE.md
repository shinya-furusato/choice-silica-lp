# AI Editing Guide

このLPはIllustrator/PDFの見た目を忠実に再現するHTMLです。AI修正では見た目の再現性を最優先し、SVG座標を不用意に変更しません。

## 編集手順
1. `src/ai-map.json` で対象セクションを特定する。
2. `src/ai-elements.json` で安全に編集できる要素か確認する。
3. 必要なら `src/ai-text-map.json` のアンカーを使う。
4. `src/sections/section-XX.html` または `src/main.html` を編集する。
5. `python build/build.py` で `index.html` を再生成する。

## 優先順位
テキスト・URL・画像参照 → 限定CSS → 限定SVG属性 → ベクター座標の順。最後の2つは明示的な必要がある場合のみ。

## 今回の固定修正
- クリック可能要素では通常の手カーソルではなく、ピンクの肉球カーソルを表示。
- CTA右端の白いヘアライン対策として、最初のCTA（section 02-03）と最終CTA（section 16-17）のSVG表示幅を2pxだけ拡張。

## 注意
- `index.html` を直接編集せず、必ず `src/` を編集してビルドする。
- 科学・健康・数値・専門家コメントは承認済み原稿に基づく場合のみ変更する。
