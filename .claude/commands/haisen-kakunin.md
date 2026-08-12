---
description: MFRC522とI2C LCD1602の配線表・注意点をチェックリスト形式で表示する
---

`docs/requirements.md`の「5. ハードウェア構成・配線」セクションと`README.md`の配線図を読み、以下を日本語のチェックリスト形式で表示してください。

- MFRC522の各ピン(3.3V/RST/GND/IRQ/MISO/MOSI/SCK/SDA)がどのGPIOに繋がるべきか
- I2C LCD1602の各ピン(GND/VCC/SDA/SCL)がどのGPIOに繋がるべきか
- MFRC522は3.3V専用で5Vを絶対に繋がないこと
- LCDのI2Cアドレスが0x27/0x3Fのどちらの可能性もあり、`tools/i2c_scan.py`で確認できること

ファイルの内容と食い違う配線をユーザーが口頭で言ってきた場合は、`docs/requirements.md`とREADME.mdを正として指摘すること。
