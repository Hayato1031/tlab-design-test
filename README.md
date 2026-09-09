# Takeda Lab. — Design prototypes

[3案を比較する](https://hayato1031.github.io/tlab-design-test/)

白基調の研究室ホームページを比較するためのプロトタイプです。

- A: 立体アートとタイポグラフィ
- B: 写真とタイポグラフィ
- C: 動く点群アート

研究テーマは約5.8秒ごとに自動で切り替わります。手動のスライド操作はありません。研究領域のリンクは、その領域の説明を開きます。動きを減らす端末設定では静止表示になります。

ページ下部は研究領域、活動の流れ、制作記録の掲載スペース、研究室情報、参加案内、問い合わせで構成しています。研究成果・活動写真は差し替え用の枠です。

## ファイル

- `index.html`: 3案の比較
- `takeda-kinetic-a.html` / `b.html` / `c.html`: 各デザイン（実ファイル名はすべて `takeda-kinetic-` で始まります）
- `takeda-kinetic.js`: 自動切り替え、点群の描画、ページ内ナビゲーション
- `takeda-kinetic.css`: トップの表現
- `takeda-page.css`: ページ下部
- `takeda-visual.css`: 共通のベーススタイル
- `assets/`: 画像・フォント

## ローカル表示

このディレクトリで `python3 -m http.server 8000` を実行し、ブラウザで `http://localhost:8000/` を開いてください。ビルドは不要です。

## 公開

GitHub Pagesで `main` ブランチのルート `/` を公開します。`.nojekyll` を同梱しており、静的ファイルをそのまま配信します。

## 内容・素材

研究内容と連絡先は、提供された[2026年度春学期「研究会Ａ」シラバス](https://gslbs.keio.jp/syllabus/detail?ttblyr=2026&entno=03720&lang=jp)を要約しています。デザイン検討用で、実運用の公式サイトではありません。

キャンパス写真は提供素材。生成した写真と立体アートは仮イメージで、実際の研究成果ではありません。[生成記録](仮画像の生成記録.md)にプロンプトを記載しています。

OutfitとM PLUS 1はSIL Open Font Licenseに基づき同梱しています。ライセンスは `assets/fonts/` を参照してください。
