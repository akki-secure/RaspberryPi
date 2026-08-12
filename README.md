# RFIDスマートロック（Raspberry Pi Pico WH / MicroPython）

MFRC522(RFIDリーダー)でタグを検知し、登録済みのUIDであればサーボモーターを回して
「解錠」動作を行うプロジェクトです。フィードバックは現時点ではシリアルログのみで、
LCD表示は後日の拡張として予定しています。

詳しい要件は [docs/requirements.md](docs/requirements.md) を参照してください。

## 必要なもの
- Raspberry Pi Pico WH
- MFRC522 RFIDモジュール（RC522）＋ RFIDカードまたはキーフォブ
- 9Gサーボモーター
- ブレッドボード・ジャンパー線
- Windows機（Thonnyインストール用）とMac（コード作成用）

## 配線図（Pico WH 物理ピン配置）

Pico WHを基板の部品面(USB端子が上)にして見たときの、実際のピン配置(1〜40番)です。
使用するピンのみ、接続先を右側に記載しています。

```
                        [USB]
   1  GP0                                   VBUS  40  → サーボ VCC(赤)
   2  GP1                                   VSYS  39
   3  GND                                    GND  38  → サーボ GND(茶)
   4  GP2                                3V3_EN   37
   5  GP3                              3V3(OUT)   36  → MFRC522 3.3V
   6  GP4                            ADC_VREF     35
   7  GP5                                  GP28   34
   8  GND                                   GND   33
   9  GP6                                  GP27   32
  10  GP7                                  GP26   31
  11  GP8                                   RUN   30
  12  GP9                                  GP22   29
  13  GND                                   GND   28
  14  GP10                                 GP21   27
  15  GP11                                 GP20   26  → MFRC522 RST
  16  GP12                                 GP19   25  → MFRC522 MOSI
  17  GP13                                 GP18   24  → MFRC522 SCK
  18  GND                                   GND   23  → MFRC522 GND
  19  GP14                                 GP17   22  → MFRC522 SDA(SS/CS)
  20  GP15 → サーボ 信号線(橙/黄)             GP16   21  → MFRC522 MISO
```

### 配線表（物理ピン番号つき）

**MFRC522 (SPI0)**
| MFRC522ピン | Pico WH 物理ピン番号 | GPIO |
|---|---|---|
| 3.3V | 36 | 3V3(OUT) |
| RST | 26 | GP20 |
| GND | 23 | GND |
| IRQ | 未接続(NC) | — |
| MISO | 21 | GP16 |
| MOSI | 25 | GP19 |
| SCK | 24 | GP18 |
| SDA(SS/CS) | 22 | GP17 |

**9Gサーボモーター**
| サーボ線 | Pico WH 物理ピン番号 | GPIO/電源 |
|---|---|---|
| VCC(赤) | 40 | VBUS(5V) |
| GND(茶) | 38 | GND |
| 信号線(橙/黄) | 20 | GP15 |

**⚠️ 注意**:
- MFRC522は3.3V専用です。5Vに接続すると壊れます。VCCは必ず物理36番ピン(`3V3(OUT)`)に接続してください。
- サーボモーターの電源は物理36番ピン(`3V3(OUT)`)ではなく物理40番ピン(`VBUS`, 5V)から取ってください。3V3ピンからだと電流不足で誤動作する場合があります。

## 開発の全体フロー

コード作成用のMacと、Pico書き込み用のWindows機が別なので、GitHubリポジトリを介してファイルをやり取りします。

```mermaid
flowchart LR
    A[Mac: Cursor/Claude Code<br>コードを編集] -->|git push| B[(GitHub<br>akki-secure/RaspberryPi)]
    B -->|git clone / pull| C[Windows機]
    C -->|Thonnyで開く| D[Thonny]
    D -->|ファイル転送・実行| E[Raspberry Pi Pico WH]
    E -->|シリアル出力| D
```

## セットアップ手順（Windows機・Thonny）

1. [Thonny公式サイト](https://thonny.org/)からインストーラーをダウンロードしてインストールする
2. Pico WHをUSBケーブルでWindows機に接続する
3. Thonnyを起動し、右下のインタプリタ選択から「MicroPython (Raspberry Pi Pico)」を選ぶ（初回はPico側にMicroPythonファームウェアの書き込みが必要な場合があります。Thonnyの案内に従ってください）
4. GitHubリポジトリをWindows機にclone、または最新をpullする
   ```
   git clone https://github.com/akki-secure/RaspberryPi.git
   ```
5. Thonnyの「ファイル」パネルで、ローカルの`src/lib/mfrc522.py`と`src/logic.py`を、Pico側の`/lib`フォルダへアップロードする（`/lib`フォルダがなければ作成する）
6. `src/main.py`をPico側のルート（`/`）へ`main.py`という名前でアップロードする
7. Thonnyで`main.py`を開き、実行ボタン（▶）を押す
8. シェル(シリアル出力)に`{"ts": ..., "level": "INFO", "event": "startup"}`のようなログが出れば起動成功

## タグの登録方法

1. `tools/uid_hyouji.py`をThonnyで開いて実行する（転送不要）
2. 登録したいRFIDタグをMFRC522にかざす
3. シリアル出力に表示されたUID（例: `04A1B2C3`）を`src/logic.py`の`許可UIDリスト`に追加する
   ```python
   許可UIDリスト = [
       "04A1B2C3",
   ]
   ```
4. `src/logic.py`をPicoの`/lib`へ再アップロードし、`main.py`を再実行する

## 動作確認
1. 登録済みのRFIDタグ（カードまたはキーフォブ）をMFRC522にかざす
2. サーボモーターが解錠角度まで回転し、約3秒後に施錠角度へ戻る
3. Thonnyのシェルに`tag_detected`→`access_granted`→`unlocked`→`locked`のログが出る
4. 未登録のタグをかざすと、`tag_detected`→`access_denied`のログが出てサーボは動かない

## フォルダ構成
```
RaspberryPi/
├── README.md
├── docs/requirements.md      # 要件定義書
├── src/
│   ├── main.py                # Pico実行エントリ
│   ├── logic.py                # ハードウェア非依存ロジック(日本語関数名)
│   └── lib/                    # 外部OSSライブラリ(MITライセンス、出典はファイル先頭に明記)
├── tests/                      # PC側pytest
├── tools/uid_hyouji.py         # タグのUID確認用(Pico上で直接実行)
├── .claude/commands/           # Claude Codeスラッシュコマンド
└── requirements-dev.txt        # PC側テスト・静的解析用
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
LCD表示による認証結果の可視化、複数タグの識別表示、施錠状態の永続化などの機能追加を行った場合は、このREADMEの配線図・フォルダ構成、および`docs/requirements.md`を必ず更新してください。API化やWeb連携など機能が拡張された場合は、その時点でAPI仕様書等を別途追加します。
