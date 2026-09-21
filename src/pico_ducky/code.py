"""Pico Ducky 注入デモ用エントリポイント(Raspberry Pi Pico WH / CircuitPython専用)。

【教育目的専用】自分が所有・管理するWindows機/隔離VM以外では絶対に実行しないこと。
他人のPC・業務PCなどへの無断実行は不正アクセス・不正指令電磁的記録に関する罪に
該当しうる。

配置先(Windows機・Explorerでコピー):
  - このファイル(code.py)          -> CIRCUITPYドライブの直下
  - lib/adafruit_hid/              -> CIRCUITPYドライブの lib/ フォルダ

動作: USBに挿すと自動実行される。安全のため
  1. 5秒待機する(挿した瞬間の暴発を防ぐ安全マージン。必須)
  2. 固定文字列を1回だけタイプする
  3. ループしない(2回目以降は挿し直すまで何も起きない。これが安全設計の要)

実験手順はREADME.mdの「注入デモの使い方」を参照(Thonnyのエディタに
フォーカスを合わせた状態でPico WHを挿す)。
"""

import time

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

待機秒数 = 5  # 挿してすぐ暴発しないための安全マージン(変更しないこと)
タイプする文字列 = "Hello from Pico Ducky (educational demo)"

time.sleep(待機秒数)

kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

# layout.write()は英数字・半角記号のみ対応(日本語は送信できない)
layout.write(タイプする文字列)

# ここでプログラムは終了する。whileループにしないことで、
# 「挿したら1回だけ動く」という予測可能な挙動を保つ。
