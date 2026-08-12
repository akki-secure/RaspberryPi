"""RFIDタグ検知→LCD表示のメインループ（Raspberry Pi Pico WH / MicroPython専用）。

Thonnyでの転送先:
  - このファイル(main.py)          -> Picoのルート
  - lib/ 配下のファイルとlogic.py  -> Picoの /lib
Picoは/libを自動的にimport検索パスへ含めるため、以下のimportは
"lib.xxx"ではなく"xxx"というフラットな書き方にしている。
配線はREADME.mdの配線表を参照。
"""

import time
from machine import Pin, SPI, I2C  # noqa: F401  (SPIはMFRC522クラス内部で使用)

from mfrc522 import MFRC522
from i2c_lcd import I2cLcd
from logic import UIDを整形する, 表示メッセージを生成する, ログを組み立てる

I2Cアドレス候補 = (0x27, 0x3F)
LCD行数 = 2
LCD桁数 = 16


def ログ出力(level, event, **kwargs):
    print(ログを組み立てる(level, event, time.ticks_ms(), **kwargs))


def LCDを初期化する():
    i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
    見つかったアドレス = i2c.scan()
    for 候補 in I2Cアドレス候補:
        if 候補 in 見つかったアドレス:
            return I2cLcd(i2c, 候補, LCD行数, LCD桁数)
    raise RuntimeError("LCDのI2Cアドレスが見つかりません: {}".format(見つかったアドレス))


def RFIDリーダーを初期化する():
    return MFRC522(sck=18, mosi=19, miso=16, rst=20, cs=17)


def タグを検知したら表示する(rdr, lcd):
    (stat, _tag_type) = rdr.request(rdr.REQIDL)
    if stat != rdr.OK:
        return False

    (stat, raw_uid) = rdr.anticoll()
    if stat != rdr.OK:
        return False

    uid = UIDを整形する(raw_uid)
    メッセージ = 表示メッセージを生成する()

    try:
        lcd.clear()
        lcd.putstr(メッセージ)
        ログ出力("INFO", "tag_detected", uid=uid)
        ログ出力("INFO", "lcd_write_ok", message=メッセージ)
    except Exception as e:
        ログ出力("ERROR", "lcd_write_error", uid=uid, error=str(e))

    return True


def main():
    ログ出力("INFO", "startup")

    try:
        lcd = LCDを初期化する()
    except Exception as e:
        ログ出力("ERROR", "lcd_init_error", error=str(e))
        raise

    try:
        rdr = RFIDリーダーを初期化する()
    except Exception as e:
        ログ出力("ERROR", "rfid_init_error", error=str(e))
        raise

    ログ出力("INFO", "ready")

    while True:
        try:
            タグを検知したら表示する(rdr, lcd)
        except Exception as e:
            ログ出力("ERROR", "unexpected_error", error=str(e))
        time.sleep_ms(200)


if __name__ == "__main__":
    main()
