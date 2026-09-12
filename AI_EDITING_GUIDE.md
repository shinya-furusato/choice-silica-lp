# AI Editing Guide

このLPは Illustrator / PDF の見た目を高精度に維持することを最優先にした構造です。AI編集では、再現性を壊さずに必要箇所だけを安全に修正することを目的とします。

## 基本方針

1. `src/ai-map.json` でユーザーの指示に対応するセクションを特定する。
2. `src/ai-elements.json` でそのセクション内の安全な編集対象とリスクを確認する。
3. `src/ai-text-map.json` で見出し・本文・出典・数値・CTAなどの具体的な意味単位を特定する。
4. 実際の修正は `src/sections/section-XX.html`、必要に応じて `src/styles.css` / `src/main.html` に行う。
5. 生成物である `index.html` は直接編集しない。
6. 修正後は GitHub Actions の `Build ecforce index.html` により `index.html` を自動再生成する。
7. ビルド成功を確認して完了とする。

## 3階層の意味

- 第1階層 `ai-map.json`：どのセクションかを特定する。
- 第2階層 `ai-elements.json`：その中のどの種類の要素を触ってよいか判断する。
- 第3階層 `ai-text-map.json`：実際の見出し・本文・出典・数値・CTAを意味名でピンポイント指定する。

例：ユーザーが「シリカの加齢グラフの出典だけ変えて」と指示した場合、`silica-age-related-decline` → `silica-decline-source` の順に解決し、出典表記だけを対象にする。

## テキスト変更で重要なこと

PDF由来のテキストは、見た目を描画する SVG `<text>` と、選択・アクセシビリティ用の `.lp-selection-text` が対になっていることがあります。コピー変更時は原則として両方を同じ内容に更新します。

通常の文章修正では、`x` / `y` / `viewBox` / `transform` / `clipPath` / `path` / `paint-order` などの幾何情報は変更しません。文章量が大きく変わり、明らかにレイアウトへ影響する場合のみ、別途レイアウト調整として扱います。

`ai-text-map.json` の `text_contains` は、対象セクション内で最小の一致テキスト要素を探すためのアンカーです。`intent` は、完全一致文字列が安全に固定できない要素を意味で特定するための補助情報です。

## 画像変更

画像差し替えは可能な限り `image.lp-asset` の `href` だけを変更します。`x` / `y` / `width` / `height` は元の構図を維持したい場合は触りません。

## CTA・リンク変更

購入先などのURL変更は `a[href]` の属性変更を優先します。CTAセクションのリンクにはビルド時に `data-ai-name` が付くため、`ai-text-map.json` から直接特定できます。見た目を変える必要がないURL差し替えではSVGやCSSを変更しません。

## 科学・健康・数値表現

シリカ含有量、加齢グラフ、水分量、専門家コメントなど、数値・科学・健康に関する表現は、承認済みの根拠またはユーザーから明示された新しい資料がある場合だけ内容を変更します。デザインだけの依頼では主張を強めたり補ったりしません。

`ai-text-map.json` では、この種の要素を `paired-text-edit-high-risk` として識別しています。

## AI向けの編集優先順位

原則は次の順です。

`テキスト / URL / 画像参照` → `CSSによる限定的な補正` → `SVG要素の限定修正` → `ベクター形状・座標の変更`

右に行くほど見た目の再現性へ影響するため、ユーザーの明確な指示がある場合だけ行います。

## 指示例

- 「シリカの加齢グラフの出典だけ変えて」
  - `silica-age-related-decline` → `silica-decline-source` を特定し、出典テキストのみを同期更新。
- 「シリカ75mg/Lの数値だけ変えて」
  - `natural-minerals-and-silica-75mg` → `silica-75mg-claim` を特定し、承認済み数値がある場合のみ更新。
- 「弁護士監修の文章だけ調整して」
  - `support-costs-and-transparency` → `lawyer-supervision-copy` を特定し、法務上の意味を変えない範囲で編集。
- 「最初の天然水購入ボタンのリンクを変えて」
  - `first-natural-water-cta-link-1` の `href` のみ変更。
- 「九重の説明を短くして」
  - `kuju-source-and-natural-filtration` 内の `kuju-mountains-copy` / `natural-filtration-copy` を対象に、SVGテキストと選択テキストの両方を更新。
- 「CTA右端の白線を直して」
  - `src/styles.css` の限定的な補正を優先し、元のベクター座標は極力触らない。

この運用により、PDF校了時の見た目を基準にしながら、校了後の部分修正をAIから安全に行える状態を維持します。
