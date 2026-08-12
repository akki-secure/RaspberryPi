import json

from logic import (
    UIDを整形する,
    ログを組み立てる,
    認証する,
    角度をパルス幅nsに変換する,
)


def test_UIDを整形する_バイト列を16進文字列に変換する():
    assert UIDを整形する([0x04, 0xA1, 0xB2, 0xC3]) == "04A1B2C3"


def test_UIDを整形する_1桁の値もゼロ埋めされる():
    assert UIDを整形する([0x00, 0x01, 0x0F]) == "00010F"


def test_認証する_許可リストに含まれていればTrue():
    assert 認証する("04A1B2C3", ["04A1B2C3", "11223344"]) is True


def test_認証する_許可リストに含まれていなければFalse():
    assert 認証する("DEADBEEF", ["04A1B2C3", "11223344"]) is False


def test_認証する_許可リストが空ならFalse():
    assert 認証する("04A1B2C3", []) is False


def test_角度をパルス幅nsに変換する_0度は最小パルス幅():
    assert 角度をパルス幅nsに変換する(0, min_us=500, max_us=2400) == 500_000


def test_角度をパルス幅nsに変換する_180度は最大パルス幅():
    assert 角度をパルス幅nsに変換する(180, min_us=500, max_us=2400) == 2_400_000


def test_角度をパルス幅nsに変換する_90度は中間のパルス幅():
    assert 角度をパルス幅nsに変換する(90, min_us=500, max_us=2400) == 1_450_000


def test_角度をパルス幅nsに変換する_範囲外は0から180にクランプされる():
    assert 角度をパルス幅nsに変換する(-10, min_us=500, max_us=2400) == 500_000
    assert 角度をパルス幅nsに変換する(200, min_us=500, max_us=2400) == 2_400_000


def test_ログを組み立てる_JSON形式で必須項目が含まれる():
    line = ログを組み立てる("INFO", "access_granted", 12345, uid="04A1B2C3")
    record = json.loads(line)
    assert record == {
        "ts": 12345,
        "level": "INFO",
        "event": "access_granted",
        "uid": "04A1B2C3",
    }


def test_ログを組み立てる_kwargsなしでも動く():
    line = ログを組み立てる("ERROR", "rfid_init_error", 0)
    record = json.loads(line)
    assert record == {"ts": 0, "level": "ERROR", "event": "rfid_init_error"}
