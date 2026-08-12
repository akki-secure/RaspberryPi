import json

from logic import UIDを整形する, 表示メッセージを生成する, ログを組み立てる


def test_UIDを整形する_バイト列を16進文字列に変換する():
    assert UIDを整形する([0x04, 0xA1, 0xB2, 0xC3]) == "04A1B2C3"


def test_UIDを整形する_1桁の値もゼロ埋めされる():
    assert UIDを整形する([0x00, 0x01, 0x0F]) == "00010F"


def test_表示メッセージを生成する_固定でHelloWorldを返す():
    assert 表示メッセージを生成する() == "Hello World!"


def test_ログを組み立てる_JSON形式で必須項目が含まれる():
    line = ログを組み立てる("INFO", "tag_detected", 12345, uid="04A1B2C3")
    record = json.loads(line)
    assert record == {
        "ts": 12345,
        "level": "INFO",
        "event": "tag_detected",
        "uid": "04A1B2C3",
    }


def test_ログを組み立てる_kwargsなしでも動く():
    line = ログを組み立てる("ERROR", "lcd_init_error", 0)
    record = json.loads(line)
    assert record == {"ts": 0, "level": "ERROR", "event": "lcd_init_error"}
