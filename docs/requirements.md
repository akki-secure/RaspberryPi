# 要件定義書 - RFIDスマートロック

このファイルはREADME.mdとは別に、本プロジェクトの要件をまとめたものです。

## 1. 目的
Raspberry Pi Pico WHに接続したMFRC522(RFIDリーダー)でRFIDタグを検知し、
登録済みのUIDであればサーボモーターを回して「解錠」動作を行う。

## 2. 対象ユーザー
Python・電子工作ともに未経験のユーザー。配線・セットアップ手順は前提知識なしで再現できることを重視する。

## 3. 機能要件
| ID | 内容 |
|---|---|
| F1 | MFRC522でRFIDタグ(カード/キーフォブ)を検知できること |
| F2 | 検知したタグのUIDが、コード中の許可UIDリストに含まれるか判定できること |
| F3 | 許可リストに含まれる場合、サーボモーターを解錠角度まで回転させ、一定時間後に施錠角度へ戻すこと |
| F4 | 許可リストに含まれない場合、サーボは動かさず警告ログのみ出すこと |
| F5 | タグ検知時・認証結果・解錠/施錠・起動時・エラー時にシリアル出力へ構造化ログを出すこと |
| F6 | タグのUIDを確認するための補助ツール(`tools/uid_hyouji.py`)を提供すること |

## 4. 非機能要件
| ID | 内容 |
|---|---|
| N1 | SPI初期化・サーボ初期化に失敗してもプログラムが無限クラッシュせず、ログを出して停止すること |
| N2 | Picoのフラッシュ書き込み回数を抑えるため、ログは常時ファイル保存せずシリアル出力のみとすること |
| N3 | 破壊的操作（ファイル一括削除・フラッシュ消去等）を行うコードを含まないこと |
| N4 | 許可UIDリストはコード(`src/logic.py`)に直接記述する方式とし、外部ファイルへの永続化は現時点で行わないこと |

## 5. ハードウェア構成・配線
ボード: Raspberry Pi Pico WH / 言語: MicroPython

### Pico WH 物理ピン配置（使用ピンのみ）
Pico WHを基板の部品面(USB端子が上)にして見たときの、実際のピン配置(1〜40番)です。

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

注意:
- MFRC522は3.3V専用。5Vを絶対に接続しないこと（破損の原因）。
- サーボモーターの電源はVBUS(物理40番, 5V)から取ること。3V3(OUT)は電流不足で誤動作する場合がある。

## 6. 開発環境・ファイル受け渡し
- コード作成: Mac上のCursor(Claude Code)
- Pico転送・実行: 別のWindows機のThonny
- 両者はGitHubリポジトリ(`https://github.com/akki-secure/RaspberryPi.git`)経由でファイルを受け渡す（Mac側でpush→Windows側でclone/pull）

## 7. 構造化ログ設計
出力先はUSBシリアル(print)、JSON Lines形式。`ts`はPico起動からの経過ミリ秒(`time.ticks_ms()`)。

- 運用ログ（INFO）: `startup`, `ready`, `tag_detected`, `access_granted`, `unlocked`, `locked`
- 警告ログ（WARNING）: `access_denied`
- 監視ログ（ERROR）: `rfid_init_error`, `servo_init_error`, `unexpected_error`

出力例:
```
{"ts": 12345, "level": "INFO", "event": "access_granted", "uid": "04A1B2C3"}
```

## 8. ガードレール
- Pico上のファイル削除・フラッシュ一括消去など破壊的操作は一切実装しない
- Thonnyでファイルを転送する際は、既存ファイルを誤って上書き・削除しないよう確認する
- 未登録タグ検知時はサーボを一切動作させない(施錠状態を維持する)

## 9. テスト方針
- PC側（CPython, `.venv`）で`pytest tests/`を実行し、`src/logic.py`のハードウェア非依存関数（UID整形・認証判定・サーボ角度→パルス幅変換・ログ組み立て）を検証する
- 静的解析は`ruff check src tests`をPC側で実行する（`src/lib`配下は外部OSSライブラリのため対象外）
- 実機動作（RFID検知→サーボ解錠）はハードウェア依存のため自動テストできない。以下の手動確認チェックリストに従う

### 手動確認チェックリスト（Thonny上で実施）
1. `src/lib/mfrc522.py`と`src/logic.py`をPicoの`/lib`へ転送する
2. `src/main.py`をPicoのルート(`/`)へ転送する
3. Thonnyで`main.py`を実行し、シリアル出力に`startup`→`ready`のログが出ることを確認する
4. 登録済みRFIDタグをMFRC522にかざし、サーボが解錠角度まで回転し、約3秒後に施錠角度へ戻ることを確認する
5. シリアル出力に`tag_detected`→`access_granted`→`unlocked`→`locked`のログが出ることを確認する
6. 未登録タグをかざし、サーボが動かず`access_denied`のログのみ出ることを確認する
7. うまくいかない場合は`tools/uid_hyouji.py`を実行し、タグのUIDが正しく読み取れているか確認する

### テスト実行時間の目安
`pytest`は通常数秒以内に完了する規模。**30分以上かかっている場合はフリーズしている可能性が高いため、実行を止めてユーザーに確認すること。**
