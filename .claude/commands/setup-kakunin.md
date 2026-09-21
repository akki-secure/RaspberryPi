---
description: CircuitPythonの書き込み手順とcode.py/libの配置先チェックリストを表示する
---

`README.md`の「CircuitPythonのインストール手順」「ファイル配置手順」セクションを読み、以下を日本語のチェックリスト形式で表示してください。

- Pico WHのBOOTSELボタンを押しながらUSB接続し、`RPI-RP2`ドライブへ`.uf2`をコピーする手順
- 再起動後、`CIRCUITPY`ドライブとして認識されることの確認
- `src/pico_ducky/code.py` を `CIRCUITPY` ドライブ直下へ `code.py` としてコピーすること
- `lib/adafruit_hid/` を `CIRCUITPY/lib/` へコピーすること
- 実行対象は自分が所有・管理するWindows機/隔離VMに限定すること（README冒頭の利用範囲の注意を必ず併記する）

ファイルの内容と食い違う手順をユーザーが口頭で言ってきた場合は、`README.md`と`docs/requirements.md`を正として指摘すること。
