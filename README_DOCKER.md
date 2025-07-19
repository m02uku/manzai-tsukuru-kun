# DockerでGemini Webアプリを実行する手順

## 1. イメージのビルド
```
docker build -t gemini-app .
```

## 2. コンテナの起動（APIキーを環境変数で渡す例）
```
docker run -d -p 5000:5000 -e GEMINI_API_KEY=あなたのAPIキー gemini-app
```

## 3. ブラウザでアクセス
http://localhost:5000

## 備考
- `.env` はDockerイメージには含めません。APIキーは `-e` オプションで渡してください。
- Renderでも同様に環境変数 `GEMINI_API_KEY` を設定すれば動作します。

## 4. コンテナの再ビルドと起動
docker stop gemini-app && docker rm gemini-app && docker build -t gemini-app . && docker run -d -p 5000:5000 --name gemini-app --env-file .env gemini-app