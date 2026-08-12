---
description: 構造化ログ(運用ログ・警告ログ・監視ログ)の出力フォーマットとイベント一覧を表示する
---

`docs/requirements.md`の「7. 構造化ログ設計」セクションを読み、以下を日本語で説明してください。

- ログの出力先(USBシリアル)とフォーマット(JSON Lines)
- 運用ログ(INFO)として出るイベント一覧: startup, ready, tag_detected, access_granted, unlocked, locked
- 警告ログ(WARNING)として出るイベント: access_denied
- 監視ログ(ERROR)として出るイベント一覧: rfid_init_error, servo_init_error, unexpected_error
- 実際の出力例を1つ示す

ユーザーがThonnyのシェルに出たログ内容を貼り付けてきた場合は、そのログがどのイベントに該当し、正常か異常かを判定して説明すること。
