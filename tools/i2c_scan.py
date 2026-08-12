"""LCDバックパックのI2Cアドレスを調べる補助スクリプト（Raspberry Pi Pico WH専用）。

Thonnyでこのファイルを開いてPico上で直接実行してください（転送不要）。
配線がREADME.mdの配線表通りであることを確認してから実行すること。
見つかったアドレスが0x27でも0x3Fでもない場合は、配線かLCD自体の不良を疑う。
"""

from machine import Pin, I2C

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
見つかったアドレス = i2c.scan()

if not 見つかったアドレス:
    print("I2Cデバイスが見つかりません。配線(SDA=GP0, SCL=GP1, VCC, GND)を確認してください。")
else:
    for アドレス in 見つかったアドレス:
        print("見つかったアドレス: 0x{:02X}".format(アドレス))
