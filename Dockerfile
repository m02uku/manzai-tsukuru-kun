# ベースイメージ
FROM python:3.11-slim

# 作業ディレクトリ作成
WORKDIR /app

# 依存ファイルコピー
COPY requirements.txt ./

# 依存パッケージインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションファイル・静的ファイルコピー
COPY gemini_server.py ./
COPY public ./public

# ポート設定
EXPOSE 5000

# 環境変数（必要に応じて）
# ENV GEMINI_API_KEY=YOUR_GEMINI_API_KEY

# サーバー起動コマンド
CMD ["python", "gemini_server.py"]
