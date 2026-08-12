# 要件定義書 - RFIDタグ検知→LCD表示

このファイルはREADME.mdとは別に、本プロジェクトの要件をまとめたものです。

## 1. 目的
Raspberry Pi Pico WHに接続したMFRC522(RFIDリーダー)がタグを検知したら、I2C接続のLCD1602に"Hello World!"と表示する。

## 2. 対象ユーザー
Python・電子工作ともに未経験のユーザー。配線・セットアップ手順は前提知識なしで再現できることを重視する。

## 3. 機能要件
| ID | 内容 |
|---|---|
| F1 | MFRC522でRFIDタグ(カード/キーフォブ)を検知できること |
| F2 | タグ検知時、LCD1602に"Hello World!"を表示すること |
| F3 | タグ検知のたびにLCD表示をクリアしてから再描画すること |
| F4 | 起動時・タグ検知時・エラー時にシリアル出力へ構造化ログを出すこと |

## 4. 非機能要件
| ID | 内容 |
|---|---|
| N1 | SPI/I2C初期化に失敗してもプログラムが無限クラッシュせず、ログを出して停止/リトライすること |
| N2 | Picoのフラッシュ書き込み回数を抑えるため、ログは常時ファイル保存せずシリアル出力のみとすること |
| N3 | 破壊的操作（ファイル一括削除・フラッシュ消去等）を行うコードを含まないこと |

## 5. ハードウェア構成・配線
ボード: Raspberry Pi Pico WH / 言語: MicroPython

**MFRC522 (SPI0)**
| MFRC522ピン | Pico WH GPIO |
|---|---|
| 3.3V | 3V3(OUT) |
| RST | GP20 |
| GND | GND |
| IRQ | 未接続(NC) |
| MISO | GP16 |
| MOSI | GP19 |
| SCK | GP18 |
| SDA(SS/CS) | GP17 |

**I2C LCD1602 (PCF8574バックパック, I2C0)**
| LCDバックパックピン | Pico WH GPIO |
|---|---|
| GND | GND |
| VCC | VBUS(5V) |
| SDA | GP0 |
| SCL | GP1 |

注意:
- MFRC522は3.3V専用。5Vを絶対に接続しないこと（破損の原因）。
- LCDのI2Cアドレスは個体差で0x27または0x3Fになる。`tools/i2c_scan.py`で確認できる。
- LCD上のコントラスト調整用可変抵抗で表示が見えない場合は調整すること。

## 6. 開発環境・ファイル受け渡し
- コード作成: Mac上のCursor(Claude Code)
- Pico転送・実行: 別のWindows機のThonny
- 両者はGitHubリポジトリ(`https://github.com/akki-secure/RaspberryPi.git`)経由でファイルを受け渡す（Mac側でpush→Windows側でclone/pull）

## 7. 構造化ログ設計
出力先はUSBシリアル(print)、JSON Lines形式。`ts`はPico起動からの経過ミリ秒(`time.ticks_ms()`)。

- 運用ログ（INFO）: `startup`, `ready`, `tag_detected`, `lcd_write_ok`
- 監視ログ（ERROR）: `lcd_init_error`, `rfid_init_error`, `lcd_write_error`, `unexpected_error`

出力例:
```
{"ts": 12345, "level": "INFO", "event": "tag_detected", "uid": "04A1B2C3"}
```

## 8. ガードレール
- Pico上のファイル削除・フラッシュ一括消去など破壊的操作は一切実装しない
- Thonnyでファイルを転送する際は、既存ファイルを誤って上書き・削除しないよう確認する

## 9. テスト方針
- PC側（CPython, `.venv`）で`pytest tests/`を実行し、`src/logic.py`のハードウェア非依存関数（UID整形・表示メッセージ生成・ログ組み立て）を検証する
- 静的解析は`ruff check src tests`をPC側で実行する（`src/lib`配下は外部OSSライブラリのため対象外）
- 実機動作（RFID検知→LCD表示）はハードウェア依存のため自動テストできない。以下の手動確認チェックリストに従う

### 手動確認チェックリスト（Thonny上で実施）
1. `src/lib/*.py`と`src/logic.py`をPicoの`/lib`へ転送する
2. `src/main.py`をPicoのルート(`/`)へ転送する
3. Thonnyで`main.py`を実行し、シリアル出力に`startup`→`ready`のログが出ることを確認する
4. RFIDタグをMFRC522にかざし、LCDに"Hello World!"が表示されることを確認する
5. シリアル出力に`tag_detected`と`lcd_write_ok`のログが出ることを確認する
6. うまくいかない場合は`tools/i2c_scan.py`を実行し、LCDのI2Cアドレスを確認する

### テスト実行時間の目安
`pytest`は通常数秒以内に完了する規模。**30分以上かかっている場合はフリーズしている可能性が高いため、実行を止めてユーザーに確認すること。**
