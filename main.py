from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# OpenAIクライアント（新しいSDK形式）
client = openai.OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)

@app.route("/")
def index():
    return "LINE WORKS Bot is running!"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        return "✅ GETリクエスト受信成功"

    # POSTの処理
    data = request.json
    print("🔥 受信したWebhook内容:", data)

    # LINE WORKSの形式に合わせて取得
    user_text = data.get("content", {}).get("text", "")

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "あなたは【つなぐファーム】アップデートのプロジェクトに関する質問に答えるAIです。現在の要点は以下の通りです：\n・新ハウス（50m×18m）の増築が完了。今後もアップデート予定。\n・アクアポニックス栽培（レタス＋ティラピア）を通年で実施。\n・冬はティラピアからニジマスに切り替え。\n・加温は太陽熱温水＋蓄熱タンクによる循環加温方式。\n・SwitchBotを用いて温度・湿度によるミスト制御を自動化済み。\n・6次化商品『Fish and Fry』『レトルトカレー』を開発中。"
                },
                {
                    "role": "user",
                    "content": user_text
                }
            ]
        )
        reply_text = response.choices[0].message.content
    except Exception as e:
        print("❌ OpenAI APIエラー:", e)
        reply_text = "申し訳ありません。AIの応答中にエラーが発生しました。"

    print("🧠 OpenAIの返信:", reply_text)
    return jsonify({"content": reply_text, "type": "text"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
