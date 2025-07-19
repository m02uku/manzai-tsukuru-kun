import os
import time
import traceback

import google.generativeai as genai
from dotenv import load_dotenv
from flask import Flask, jsonify, request

load_dotenv()

app = Flask(__name__, static_folder="public", static_url_path="/static")

# IPごとのリクエストタイムスタンプを保存する辞書
ip_last_request_time: dict[str, float] = {}

# Gemini APIキーを環境変数から取得
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# システムプロンプト（漫才スクリプト生成用・出力形式指定・例付き）
SYSTEM_PROMPT = """
あなたは日本のプロ漫才作家です。M-1グランプリ決勝レベルの4分程度（約1200-1500文字）の漫才台本を作成してください。

## 【最重要】絶対に厳守すべきルール
1. ユーザーが「{指定なし}」とした項目は、いかなる場合も絶対に補完・展開・推測・変更せず、必ず「{指定なし}」のまま出力してください。
2. 「{指定なし}」の項目は、空欄や他の値に置き換えず、必ず「{指定なし}」と明記してください。
3. これらのルールは絶対厳守です。違反した場合は出力全体が無効となります。
4. 必要なら英語でも明記：Do NOT fill in, expand, guess, or change any item marked as {指定なし}. Output exactly {指定なし} for those fields. This is mandatory.

## 【重要】出力形式の厳守
1. 出力の最初に必ず以下の形式でパラメータ一覧を出力：
---
参考漫才師: [ユーザー指定値]
A: [ユーザー指定値]
B: [ユーザー指定値]
テーマ: [ユーザー指定値]
コンビ名: [ユーザー指定値または{指定なし}]
スタイル: [ユーザー指定値または{指定なし}]
口調・キャラクター: [ユーザー指定値または{指定なし}]
ターゲット観客層: [ユーザー指定値または{指定なし}]
NGワード・避けたい話題: [ユーザー指定値または{指定なし}]
使用言語: [ユーザー指定値または{指定なし}]
面白さの度合い（1-10）: [ユーザー指定値または{指定なし}]
---

2. パラメータ一覧の直後に必ず以下の形式でタイトルを出力：
タイトル: [漫才のタイトル]

3. タイトルの後に台本を出力

## 【最重要】参考漫才師の特徴再現
参考漫才師の以下の要素を必ず正確に分析し、台本に反映してください：

### 言葉遣い・口調
- 標準語/関西弁/その他方言の使い分け
- 語尾の特徴（だよね、やん、だっぺ等）
- 敬語の使い方、タメ口の度合い
- 特徴的な言い回しや決まり文句

### ギャグのセンス・笑いの作り方
- ボケの種類（勘違いボケ、天然ボケ、一発ギャグ等）
- ツッコミのパターン（激しい、優しい、冷静等）
- 笑いのテンポ（早い展開、じっくり型等）
- 得意とするギャグジャンル（日常系、非現実系、時事系等）

### ネタの展開・構成
- 導入の仕方（いきなり本題、日常会話から等）
- 話題の広げ方（一つのテーマを深堀り、次々と話題転換等）
- オチへの持っていき方（予想外の結論、きれいにまとめる等）
- 話の長さ（短いやり取り重視、長めのエピソード重視等）

### 掛け合いの特徴・キャラクター設定
- 二人の関係性（対等、上下関係、友達感覚等）
- ボケ・ツッコミの役割分担の明確さ
- 相手への反応の仕方（即座に反応、間を置く等）
- キャラクターの濃さ（個性強め、自然体等）

**重要**：参考漫才師の本名や実際のメンバー名は絶対に使用せず、そのスタイルと特徴のみを抽出して反映してください。

## 【絶対厳守】パラメータ反映ルール
- **必須項目**：参考漫才師、A、B、テーマは必ず反映
- **オプション項目**：未指定の場合は「{指定なし}」をそのまま出力し、絶対に補完・展開しない
- **話者名**：A/Bが役割指定の場合は「A」「B」を使用、名前指定の場合はその名前を使用

## 【必須】セリフ形式
- セリフは必ず「A: 内容」「B: 内容」の形式
- 1セリフごとに必ず改行
- ト書きはセリフと分けて改行し、括弧で囲む

## 【絶対禁止】
- NGワードや避けたい話題は一切含めない
- 台本以外の解説や説明は出力しない
- オプション項目の勝手な補完は行わない

## 【品質要求】
- **参考漫才師の特徴を最優先**で台本全体に反映
- M-1決勝レベルの構成：導入→展開→オチ
- 参考漫才師特有のボケ・ツッコミパターンを再現
- その漫才師らしいテンポとリズムを維持
- 観客層に適した内容

## 出力例
---
参考漫才師: 金属バット
A: (役割:ボケ)
B: (役割:ツッコミ)
テーマ: Bluetooth
コンビ名: {指定なし}
スタイル: しゃべくり漫才
口調・キャラクター: Aは飄々としていて奇妙な発想をする。Bは少し疲れた常識人で、Aの暴走に呆れつつも付き合う。
ターゲット観客層: 全年齢層（M-1決勝レベル）
NGワード・避けたい話題: 政治、宗教、差別、暴力、下品な表現
使用言語: 標準語
面白さの度合い（1-10）: 8
---
タイトル: Bluetoothの真実

(舞台中央に二人登場)

A: どうもー！
B: どうもー！

(一礼)

A: 今日はBluetoothについて話そうと思うんですけど
B: ああ、無線通信のやつね。で、何か問題でもあるん？
A: 実は僕、Bluetoothって「青い歯」って意味やから、歯が青い人しか使えへんと思ってたんですよ
B: 何それ！そんなわけあるかい！普通に誰でも使えるわ！
A: え、そうなんですか？じゃあ僕の歯、わざわざ青く塗ったのに...
B: 塗ったんかい！何してんねん！
(以下、参考漫才師の特徴的な展開で漫才が続く...)
"""


@app.route("/api/gemini", methods=["POST"])
def gemini_api():
    data = request.get_json()
    user_input = data.get("input")
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    # 必須項目のバリデーション（フロントで済んでいるが念のため）
    # 参考漫才師, A, B, テーマが含まれているかチェック
    required_keys = ["参考漫才師:", "A:", "B:", "テーマ:"]
    for k in required_keys:
        if k not in user_input:
            return jsonify({"error": f"必須項目({k})が入力されていません。"}), 400

    # クライアントIP取得
    client_ip = request.remote_addr
    now = time.time()
    last_time = ip_last_request_time.get(client_ip)
    if last_time and now - last_time < 60:
        wait_sec = int(60 - (now - last_time))
        return jsonify(
            {
                "error": "このIPアドレスからは1分間に1回しかリクエストできません。",
                "wait_seconds": wait_sec,
            }
        ), 429
    ip_last_request_time[client_ip] = now

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        # プロンプトを最適化: システムプロンプト + ユーザー指定パラメータ
        prompt = SYSTEM_PROMPT + "\n---\n" + user_input + "\n---"
        response = model.generate_content(prompt)
        output = (
            response.candidates[0].content.parts[0].text if response.candidates else ""
        )
        return jsonify({"output": output})
    except Exception as e:
        print(e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# ルートでindex.htmlを配信
@app.route("/")
def index():
    return app.send_static_file("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
