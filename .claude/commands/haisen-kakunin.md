---
description: MFRC522とサーボモーターの配線表（Pico WH物理ピン番号）・注意点をチェックリスト形式で表示する
---

`docs/requirements.md`の「5. ハードウェア構成・配線」セクションと`README.md`の配線図を読み、以下を日本語のチェックリスト形式で表示してください。

- MFRC522の各ピン(3.3V/RST/GND/IRQ/MISO/MOSI/SCK/SDA)がPico WHの何番ピン(物理ピン番号)・どのGPIOに繋がるべきか
- サーボモーターの各線(VCC/GND/信号線)がPico WHの何番ピン(物理ピン番号)・どのGPIO/電源に繋がるべきか
- MFRC522は3.3V専用で5Vを絶対に繋がないこと
- サーボモーターの電源はVBUS(物理40番、5V)から取ること。3V3(OUT)は電流不足で誤動作する場合があること

ファイルの内容と食い違う配線をユーザーが口頭で言ってきた場合は、`docs/requirements.md`とREADME.mdを正として指摘すること。
