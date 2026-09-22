# Pico Ducky検証（Raspberry Pi Pico WH / CircuitPython）

Raspberry Pi Pico WHをUSB HIDキーボードとして振る舞わせる、いわゆる「Pico Ducky」
（BadUSB）の仕組みを実際に体験し、**攻撃者がUSB経由でキー入力を注入できてしまう原理と、
それを起点にキーロガーが成立する過程を理解した上で、どう防ぐかを学ぶ**ための実験プロジェクトです。

詳しい要件は [docs/requirements.md](docs/requirements.md) を参照してください。

> ⚠️ **利用範囲を必ず守ってください**
> - 実行対象は**自分が所有・管理するWindows機、または隔離VM**に限定してください。
> - 他人のPC・共用PC・業務PCなどへの無断実行は絶対に行わないでください
>   （不正アクセス禁止法・不正指令電磁的記録に関する罪に抵触しうる行為です）。
> - 本プロジェクトのコードはネットワーク送信機能を持たず、ペイロードもループしない
>   （1回挿すと1回だけ動作する）安全設計にしていますが、改変して悪用しないでください。

## 必要なもの
- Raspberry Pi Pico WH
- USBケーブル
- 検証用のWindows機（自分が所有・管理するもの、または隔離VM）
- Thonny（注入デモの入力先アプリとして使用。CircuitPythonへのファイル配置自体はExplorerで行うため、書き込みツールとしては不要）

## HID・CIRCUITPYとは
- **HID (Human Interface Device)**: キーボードやマウスなどをUSB経由でPCに接続するための業界標準規格。「キーボードです」と名乗ったUSB機器は、本物かPico WHかをPC側が区別できず無条件で信頼してしまいます。これが「Pico Ducky」の仕組みの根本です。
- **CIRCUITPY**: Pico WHにCircuitPythonを書き込むと、Pico WHがUSBメモリのようなドライブとしてWindows機に認識されます。そのドライブ名が`CIRCUITPY`です。ここに`code.py`や`lib/`フォルダを置くだけで、Pico側への書き込みが完了します（Thonnyでの転送操作は不要）。

## CircuitPythonのインストール手順（Windows機）
1. [circuitpython.org/board/raspberry_pi_pico_w](https://circuitpython.org/board/raspberry_pi_pico_w/) から最新の`.uf2`ファイルをダウンロードする（Pico WHはPico Wと同じRP2040+CYW43構成のため、このボードページを使用します）
2. Pico WHの**BOOTSELボタンを押しながら**USBケーブルでWindows機に接続する
3. `RPI-RP2`という名前のドライブが表示されるので、ダウンロードした`.uf2`ファイルをそこへドラッグ&ドロップする
4. 自動的に再起動し、`CIRCUITPY`という名前のドライブとして認識されればインストール完了

## ファイル配置手順
1. `CIRCUITPY`ドライブ直下に、リポジトリの`src/pico_ducky/code.py`を`code.py`という名前でコピーする
2. `CIRCUITPY`ドライブに`lib`フォルダを作成し、リポジトリの`lib/adafruit_hid/`フォルダ一式をコピーする
   （出典・ライセンスは[lib/adafruit_hid/SOURCE.md](lib/adafruit_hid/SOURCE.md)を参照）
3. コピーが完了すると、`CIRCUITPY`ドライブは以下のような構成になります
   ```
   CIRCUITPY/
   ├── code.py
   └── lib/
       └── adafruit_hid/
   ```

## 注入デモの使い方
1. Windows機でThonnyを起動し、新規ファイル（未保存でよい）のエディタ画面にカーソルを置いておく
2. Pico WHをUSBケーブルでWindows機に接続する（`code.py`を保存済みであれば挿すだけで自動実行される）
3. `code.py`内の**5秒待機**の間にThonnyのエディタへフォーカスを合わせる
4. 5秒後、自動的に固定文字列（`Hello from Pico Ducky (educational demo)`）がThonnyのエディタへ入力されることを確認する
5. 1回タイプしたらプログラムは終了する（ループしない）。再度試す場合はPico WHを一度抜き、挿し直す

## キーロガーデモ（PC側）の使い方
`tools/keylogger_demo.py`は、注入されたキー入力がPC側でどのように記録されうるかを体験するための、教育目的専用のPythonスクリプトです。

1. 事前に`pip install -r requirements-dev.txt`で`pynput`をインストールする
2. `python tools/keylogger_demo.py`を手動で実行する（自動起動・常駐化は行わない）
3. 上記の注入デモを実行するか、手動でキーを押して、押下内容が記録されることを確認する
4. `Ctrl+C`で記録を停止する
5. **確認が終わったら、生成されたログファイル（`keylogger_demo_*.log`）を必ず削除する**

> このスクリプトにネットワーク送信機能はありません。記録は手元のログファイルにのみ行われます。

> **WSL2上では動作しない**: `pynput`のキーボードリスナーはOSのグローバルキーボードフックに依存するが、WSL2はWindows側の物理キーボード入力をLinuxカーネルまで橋渡ししないため、キー入力を検知できない（起動・停止メッセージは表示されるがログファイルは生成されない）。検証は本来の想定通りWindows機のPowerShell/コマンドプロンプトで行うこと。

## 防御方法（学習ゴール）
この実験を通じて理解できる防御の考え方を整理します。

- **USB HID機器は「キーボードです」と名乗るだけで信頼されてしまう**（HID規格の性質そのものが弱点）
- **Windowsのグループポリシー／USBデバイス制御ソフト**で、未知のUSBデバイスの接続を制限する
- **「USBメモリのはずがキーボードとしても認識される」複合デバイスの挙動**を検知するエンドポイント保護製品を導入する
- **信頼できないUSB機器を安易に挿さない**、という物理的な運用ルールを徹底する（USBポートの物理ロック等も有効）
- ソフトウェアキーロガー対策としては、EDR/アンチウイルスによる不審なキーボードフック検知や、重要な操作は仮想キーボード・二要素認証を併用することも有効

## 開発の全体フロー
コード作成用のMacと、Pico書き込み用のWindows機が別なので、GitHubリポジトリを介してファイルをやり取りします。

```mermaid
flowchart LR
    A[Mac: Cursor/Claude Code<br>コードを編集] -->|git push| B[(GitHub<br>akki-secure/RaspberryPi)]
    B -->|git clone / pull| C[Windows機]
    C -->|Explorerでコピー| D[CIRCUITPYドライブ]
    D -->|USB挿入で自動実行| E[Raspberry Pi Pico WH]
    E -->|HIDキー入力| F[Thonny等のフォーカス中アプリ]
```

## フォルダ構成
```
RaspberryPi/
├── README.md
├── docs/requirements.md          # 要件定義書
├── src/
│   └── pico_ducky/
│       └── code.py               # Pico実行エントリ(CircuitPython)
├── lib/
│   └── adafruit_hid/             # 外部OSSライブラリ(MITライセンス、出典はSOURCE.md参照)
├── tools/keylogger_demo.py       # PC側キーロガーデモ(手動実行)
├── tests/                        # PC側pytest(conftest.pyのみ、現状ロジックテストなし)
├── .claude/commands/             # Claude Codeスラッシュコマンド
└── requirements-dev.txt          # PC側テスト・静的解析・pynput用
```

## 開発フロー（git運用）
- `main`ブランチには直接コミット・pushしない
- 機能追加は`feature/xxx`ブランチで作業し、動作確認後に`main`へ統合する

## テスト・静的解析（PC側、Mac/Windowsどちらでも可）
```
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/pytest tests/
.venv/bin/ruff check src tests
```
`pytest`は通常数秒で完了します。**30分以上かかる場合はフリーズの可能性が高いため、実行を止めて確認してください。**

## 今後の拡張について
機能追加を行った場合は、このREADMEのフォルダ構成・使い方、および`docs/requirements.md`を必ず更新してください。特にガードレール（ループさせない・ネットワーク送信しない・実行対象を自分のWindows機/隔離VMに限定する）は緩めないでください。
