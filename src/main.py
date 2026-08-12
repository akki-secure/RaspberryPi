"""RFIDタグ認証→サーボ解錠のメインループ（Raspberry Pi Pico WH / MicroPython専用）。

Thonnyでの転送先:
  - このファイル(main.py)          -> Picoのルート
  - lib/ 配下のファイルとlogic.py  -> Picoの /lib
Picoは/libを自動的にimport検索パスへ含めるため、以下のimportは
"lib.xxx"ではなく"xxx"というフラットな書き方にしている。
配線はREADME.mdの配線表を参照。

フィードバックは現時点ではシリアルログのみ。LCD表示は後日拡張予定。
"""

import time
from machine import Pin, SPI, PWM  # noqa: F401  (SPIはMFRC522クラス内部で使用)

from mfrc522 import MFRC522
from logic import (
    UIDを整形する,
    認証する,
    角度をパルス幅nsに変換する,
    ログを組み立てる,
    施錠角度,
    解錠角度,
)

解錠保持ms = 3000


def ログ出力(level, event, **kwargs):
    print(ログを組み立てる(level, event, time.ticks_ms(), **kwargs))


def RFIDリーダーを初期化する():
    return MFRC522(sck=18, mosi=19, miso=16, rst=20, cs=17)


def サーボを初期化する():
    pwm = PWM(Pin(15))
    pwm.freq(50)
    return pwm


def サーボを角度に動かす(pwm, angle_deg):
    pwm.duty_ns(角度をパルス幅nsに変換する(angle_deg))


def タグを検知したら認証する(rdr, servo):
    (stat, _tag_type) = rdr.request(rdr.REQIDL)
    if stat != rdr.OK:
        return False

    (stat, raw_uid) = rdr.anticoll()
    if stat != rdr.OK:
        return False

    uid = UIDを整形する(raw_uid)
    ログ出力("INFO", "tag_detected", uid=uid)

    if 認証する(uid):
        ログ出力("INFO", "access_granted", uid=uid)
        サーボを角度に動かす(servo, 解錠角度)
        ログ出力("INFO", "unlocked", uid=uid)
        time.sleep_ms(解錠保持ms)
        サーボを角度に動かす(servo, 施錠角度)
        ログ出力("INFO", "locked", uid=uid)
    else:
        ログ出力("WARNING", "access_denied", uid=uid)

    return True


def main():
    ログ出力("INFO", "startup")

    try:
        rdr = RFIDリーダーを初期化する()
    except Exception as e:
        ログ出力("ERROR", "rfid_init_error", error=str(e))
        raise

    try:
        servo = サーボを初期化する()
        サーボを角度に動かす(servo, 施錠角度)
    except Exception as e:
        ログ出力("ERROR", "servo_init_error", error=str(e))
        raise

    ログ出力("INFO", "ready")

    while True:
        try:
            タグを検知したら認証する(rdr, servo)
        except Exception as e:
            ログ出力("ERROR", "unexpected_error", error=str(e))
        time.sleep_ms(200)


if __name__ == "__main__":
    main()
