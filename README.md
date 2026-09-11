# Takeda Lab. — Design prototypes

[9案を比較する](https://hayato1031.github.io/tlab-design-test/) · [H案](https://hayato1031.github.io/tlab-design-test/takeda-kinetic-h.html) · [I案](https://hayato1031.github.io/tlab-design-test/takeda-kinetic-i.html)

白基調の研究会ホームページを比較するプロトタイプです。

- **H / Campus gateway**：キャンパス写真とコンパクトな研究紹介。6領域、共同研究・交流、学生参加、成果・メンバー・アクセスへの入口を初期画面に集約。
- **I / Research atlas**：線のアートと研究領域の説明付き一覧。研究から探す入口と目的別の案内を左右に配置。
- **G / Research list**：Fをベースに成果・活動を画像なしのリストに変更。研究領域とメンバーの画像も外し、アクセスにGoogleマップを埋め込みます。
- **F / Profile & research cards**：Eの紹介・交流と参加への入口・右の縦目次と、Dの画像付き研究カード・成果・メンバー欄を組み合わせた案。
- **E / Academic profile**：[chujo.me](https://chujo.me/)を参考にした、細いヘッダー・本文中心の研究室プロフィール。上部は紹介と交流・参加への入口を左、縦並びの目次を右に配置し、本文幅も調整しています。研究内容を展開操作なしで読める構成です。
- **D / Research index**：大きなトップビジュアルを設けず、概要・研究領域・研究成果から始まる案。本文幅・余白・写真枠を調整しました。
- **A / Sculptural art**：立体アートとタイポグラフィ。
- **B / Photography**：写真とタイポグラフィ。
- **C / Generative field**：動く点群アート。

9案とも日本語・英語のページがあります。A〜Cの研究テーマは約5.8秒ごとに自動で切り替わります。手動のスライド操作はありません。動きを減らす端末設定では静止表示になります。D・E・F・Gはスライドや導入用の大きなビジュアルを持ちません。

## 共通の内容

研究会について（活動方針・制作環境）、6つの研究領域、研究成果・活動報告、メンバー、交流・参加の案内、アクセス・お問い合わせ。内部組織の「班」を紹介する構成ではありません。

共同研究・交流・取材を検討する方と、研究会への参加・履修を検討する学生の両方に、概要から専用案内へ進める入口を用意しています。問い合わせは件名付きのメールリンクです。フォームやCMSは接続していません。

教員名は既知の情報を掲載しています。学生の氏名・写真・プロフィール、研究成果、展示・発表、設備情報は掲載用の枠で、実在の人物や実績を創作していません。

## 編集と表示

- `takeda-kinetic-a.html`〜`takeda-kinetic-i.html`：日本語の各案
- `takeda-kinetic-a-en.html`〜`takeda-kinetic-i-en.html`：英語の各案
- `index.html` / `takeda-kinetic-compare.html`：9案の比較
- `takeda-kinetic-review-a.html`〜`takeda-kinetic-review-i.html`：PC・スマホのスクリーンショット比較
- `tools/build_pages.py`：共通内容と日英ページの生成元
- `tools/hero-a.html`〜`tools/hero-c.html`：A〜Cのビジュアル部分のテンプレート
- `tools/build_portals.py`：Gの本文を継承してH・Iを別ファイルに生成
- `takeda-portals.css`：H・Iの独立したトップ画面とレスポンシブのスタイル
- `tools/build_compare.py`：比較・レビュー画面の生成元
- `takeda-page.css`：共通内容とD・F案のスタイル
- `takeda-list.css`：G案の画像なしリスト・メンバー・地図のスタイル
- `takeda-editorial.css`：E案と、F案の紹介部分のスタイル
- `takeda-kinetic.css` / `takeda-visual.css`：既存ビジュアルと基本スタイル
- `takeda-kinetic.js`：自動切り替え・点群描画・ページ内ナビゲーション

生成元を編集したときは `python3 tools/build_pages.py` → `python3 tools/build_portals.py` → `python3 tools/build_compare.py` の順に を実行します。生成されたHTMLはそのまま配信でき、閲覧時のビルドは不要です。スクリーンショットは実際の画面から更新してください。

ローカルでは、このディレクトリで `python3 -m http.server 8000` を実行し、ブラウザで `http://localhost:8000/` を開きます。

GitHub Pagesは `main` ブランチのルート `/` を公開します。

## 内容・素材の出典

- 研究内容と連絡先：[2026年度春学期「研究会Ａ」シラバス](https://gslbs.keio.jp/syllabus/detail?ttblyr=2026&entno=03720&lang=jp)
- 所在地・交通案内：[慶應義塾大学 湘南藤沢キャンパス](https://www.keio.ac.jp/ja/about/campus/sfc/)
- キャンパスマップ：[大学公式マップ](https://www.keio.ac.jp/ja/about/campus/sfc/map/)
- 教員案内：[環境情報学部教員一覧](https://www.keio.ac.jp/ja/sfc-pem/faculty/ei/)

キャンパス写真は提供素材です。生成写真と立体アートは仮イメージで、実際の研究成果ではありません。[生成記録](仮画像の生成記録.md)にプロンプトを記載しています。OutfitとM PLUS 1はSIL Open Font Licenseに基づき同梱しています。ライセンスは `assets/fonts/` にあります。

E案は参考サイトの情報の読みやすさと簡潔な構成を取り入れています。参考サイトの人物情報・文章・写真・コードは転載していません。

G案のGoogleマップは[慶應SFC公式の会場アクセス案内](https://expo.sfc.keio.ac.jp/2025/ja/access/)に掲載された埋め込み先・リンクを使用しています。地図の表示にはインターネット接続が必要です。

H・Iは、初期画面で主要な流れを選べることを優先します。本文の閲覧には通常の縦スクロールを使用し、固定高さによる切り捨ては行いません。スマホでは装飾を縮小・省略し、概要と11本の目的別・情報別リンクを保持します。ユーザー提供の参考スクリーンショットは導線の考え方の参考とし、第三者サイトのロゴ・画像・文言は使用していません。
