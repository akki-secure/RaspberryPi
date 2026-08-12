"""RFIDタグのUIDを確認する補助スクリプト（Raspberry Pi Pico WH専用）。

Thonnyでこのファイルを開いてPico上で直接実行してください（転送不要）。
配線がREADME.mdの配線表通りであることを確認してから実行すること。

タグをMFRC522にかざすとUID（16進文字列）がシリアル出力される。
表示されたUIDを src/logic.py の許可UIDリストに追加すれば、
そのタグでの解錠が許可されるようになる。
"""

import time
from machine import Pin, SPI  # noqa: F401  (SPIはMFRC522クラス内部で使用)

from mfrc522 import MFRC522


def UIDを整形する(uid_bytes):
    return "".join("{:02X}".format(b) for b in uid_bytes)


rdr = MFRC522(sck=18, mosi=19, miso=16, rst=20, cs=17)
print("タグ待機中... MFRC522にRFIDタグをかざしてください")

while True:
    (stat, _tag_type) = rdr.request(rdr.REQIDL)
    if stat == rdr.OK:
        (stat, raw_uid) = rdr.anticoll()
        if stat == rdr.OK:
            print("UID: {}".format(UIDを整形する(raw_uid)))
    time.sleep_ms(200)
