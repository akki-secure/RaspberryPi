---
description: PC側の自動テスト(pytest)と静的解析(ruff)をまとめて実行する
---

以下をこの順番で実行し、結果を日本語で要約して報告してください。

1. `.venv`が無ければ `python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt` を実行する
2. `.venv/bin/ruff check src tests` を実行する（`lib`は外部OSSライブラリのため対象外）
3. `.venv/bin/pytest tests/ -v` を実行する

注意:
- pytestの実行が30分以上かかっている場合はフリーズの可能性が高いので、実行を中断してユーザーに確認すること
- テストや静的解析を通すためにテストコード自体を無意味に緩めたり削除したりしないこと
