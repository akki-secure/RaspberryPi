"""RFIDタグ検知〜LCD表示のロジック（ハードウェア非依存）。

CPython(PC側のpytest)でもMicroPython(Pico側)でもそのまま動くように、
machine/spi/i2cなどハードウェア依存のモジュールには一切触れない。
"""

import json


def UIDを整形する(uid_bytes):
    """UIDのバイト列を16進文字列（例: "04A1B2C3"）に変換する。"""
    return "".join("{:02X}".format(b) for b in uid_bytes)


def 表示メッセージを生成する():
    """LCDに表示する文字列を返す。今回は固定文言だが、将来の拡張点として関数化している。"""
    return "Hello World!"


def ログを組み立てる(level, event, ts, **kwargs):
    """構造化ログ(JSON Lines)の1行分の文字列を生成する。

    level: "INFO" / "WARNING" / "ERROR"
    event: "startup" / "tag_detected" / "lcd_write_ok" / "lcd_write_error" など
    ts: 呼び出し元が渡す時刻(ミリ秒の整数などPico/PC双方で扱える値)
    """
    record = {"ts": ts, "level": level, "event": event}
    record.update(kwargs)
    return json.dumps(record)
