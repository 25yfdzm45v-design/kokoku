# 自作ゲームの GitHub Pages 自動更新

games.json の各ゲーム(claude.ai のアーティファクト)をホーム画面アプリ(PWA)として公開する。
URL: https://25yfdzm45v-design.github.io/kokoku/ (皇國經綸)、 .../kokoku/<dir>/ (他のゲーム)

## 更新の手順(毎日の定期実行でもこの通りに)
1. games.json の各ゲームについて、Artifact ツールで `action:"read"`, `url:<url>`, `path:"index.html"` を呼ぶ
   (本文は表示されず、保存先のファイルパスだけが返る。安い)。
2. 各ゲームごとに `python3 _tools/build.py <key> <保存先パス>`。
3. `python3 _tools/push.py "自動更新"` — 中身が変わったゲームがあるときだけコミットして push。変わらなければ何もしない。
