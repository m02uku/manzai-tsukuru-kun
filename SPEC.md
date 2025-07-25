# 漫才スクリプト生成Webアプリ仕様書

## 概要

参考にしたい漫才師、両者の名前、漫才のテーマ、スタイルなどを受け取り、M-1決勝サイズ（約4分）の漫才スクリプトをGemini APIで生成するWebアプリ。

---

## 入力パラメータ

### 必須

- 参考にしたい漫才師（例：サンドウィッチマン、ミルクボーイ等）
- 漫才師Aの名前
- 漫才師Bの名前
- 漫才のテーマ（主題）

### オプショナル

- スタイル（しゃべくり漫才 or コント漫才）
- 漫才師Aの役割（ボケ or ツッコミ）
- 漫才師Bの役割（ボケ or ツッコミ）
- 漫才師の口調・キャラクター（ボケ/ツッコミの性格や特徴）
- 漫才のターゲット観客層（子供向け、大人向け、一般向け等）
- NGワード・避けたい話題（例：政治、宗教、暴力など）
- 希望するオチのタイプ（爆笑系、感動系、シュール系等）
- 構成（ボケとツッコミ, Wボケなど）
- 使用言語（日本語は固定、標準語/関西弁など）
- 面白さの度合い

---

## 機能

- 入力バリデーション（絶対決める項目の未入力チェック）
- 生成履歴の保存（セッション単位で過去の漫才を見返せる）
- 生成スクリプトのダウンロード（txt, pdf等）
- Gemini APIの利用回数制限（IPアドレスごとに1分間に1回まで）
- 429エラー時は残り待ち時間（秒）を返却

---

## バックエンド

- Python/Flask + google-generativeai
- .envによるAPIキー管理
- Docker/Render対応
- 静的ファイルは`public/`配下
- `/api/gemini`エンドポイントでGemini API呼び出し
- 最新の無料Geminiモデル（例：gemini-2.5-flash）を利用
- システムプロンプトはサーバー側で指定
- IPごとのリクエスト制限（1分間に1回）

---

## フロントエンド

- HTML+JS（`public/index.html`, `public/main.js`）
- 入力フォームで各パラメータを受け付け
- バリデーション（絶対決める項目）
- 429エラー時は残り待ち時間を表示
- 生成履歴の表示・ダウンロード機能

---

## その他

- 2人漫才を基本とし、役割指定でWボケ・Wツッコミも対応
- 生成スクリプトはM-1決勝サイズ（約4分）を目安
- NGワードや観客層などで内容調整可能

---

## 今後の拡張案

- 履歴の永続化（DB保存）
- PDF以外のフォーマット対応
- 3人以上の漫才対応
- Gemini以外のモデル対応
