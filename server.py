from flask import Flask, request, jsonify
import openai
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Allows your website to connect to this server

# Get OpenAI API key from environment variables (safer than writing it in code)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Debugging: Check if API Key is being loaded
if openai.api_key:
    print("✅ API Key Loaded Successfully!")
else:
    print("❌ API Key is MISSING! Check Render Environment Variables.")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI."},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7
        )
        return jsonify({"response": response["choices"][0]["message"]["content"]})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
