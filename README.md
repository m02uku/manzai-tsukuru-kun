# まんざいつくるくん

[まんざいつくるくん](https://manzai-tsukuru-kun.onrender.com/)

## 概要
Google Gemini APIを使い、1回の入力に対して応答を返すシンプルなWebサイトです。

- サーバー: Node.js (Express)
- クライアント: HTML + JS
- 公開: Render対応

## 使い方
1. `GEMINI_API_KEY` を環境変数で設定してください。
2. `npm install` で依存パッケージをインストール。
3. `npm start` でローカル起動。
4. Renderで公開する場合は、環境変数 `GEMINI_API_KEY` を設定してください。

## システムプロンプト
サーバー側で事前指定しています。

## ファイル構成
- `public/index.html` : フロントエンド
- `public/main.js` : フロントエンドJS
- `server.js` : サーバー/API
- `package.json` : 依存パッケージ
- `.gitignore` : git管理外ファイル

## 注意
Gemini APIキーは絶対に公開しないでください。
