from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS  # 👈 Add this
import requests

app = Flask(__name__)
CORS(app)  # 👈 Allow all cross-origin requests

API_KEY = "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"
MODEL = "mistralai/mistral-7b-instruct"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

@app.route("/")
def serve_html():
    return send_from_directory(".", "chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    data = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You help Caterpillar machine operators. Use simple words only. Answer in max 5 short points. Each point must be on a new line. Make it easy for uneducated workers to understand.Format it and increase its readability"
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

    try:
        result = response.json()
        reply = result["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({
            "error": "Failed to get response",
            "details": str(e),
            "raw": response.text
        })

if __name__ == "__main__":
    app.run(debug=True)
