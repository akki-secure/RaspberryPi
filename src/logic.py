"""RFIDスマートロックのロジック(ハードウェア非依存)。

CPython(PC側のpytest)でもMicroPython(Pico側)でもそのまま動くように、
machine/spiなどハードウェア依存のモジュールには一切触れない。
"""

import json

許可UIDリスト = [
    # ここに登録済みタグのUID(16進文字列、UIDを整形するの出力形式)を追加する
    # 例: "04A1B2C3",
]

施錠角度 = 0
解錠角度 = 90


def UIDを整形する(uid_bytes):
    """UIDのバイト列を16進文字列（例: "04A1B2C3"）に変換する。"""
    return "".join("{:02X}".format(b) for b in uid_bytes)


def 認証する(uid, 許可リスト=許可UIDリスト):
    """UIDが許可リストに含まれていればTrueを返す。"""
    return uid in 許可リスト


def 角度をパルス幅nsに変換する(angle_deg, min_us=500, max_us=2400):
    """サーボ角度(0〜180度)を、50Hz PWMのパルス幅(ナノ秒)に変換する。

    範囲外の角度は0〜180度にクランプする。
    """
    クランプ後角度 = max(0, min(180, angle_deg))
    パルス幅us = min_us + (max_us - min_us) * クランプ後角度 / 180
    return int(パルス幅us * 1000)


def ログを組み立てる(level, event, ts, **kwargs):
    """構造化ログ(JSON Lines)の1行分の文字列を生成する。

    level: "INFO" / "WARNING" / "ERROR"
    event: "startup" / "tag_detected" / "access_granted" / "access_denied" など
    ts: 呼び出し元が渡す時刻(ミリ秒の整数などPico/PC双方で扱える値)
    """
    record = {"ts": ts, "level": level, "event": event}
    record.update(kwargs)
    return json.dumps(record)
