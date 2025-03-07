from flask import Flask, request, jsonify
import openai
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Allows your website to connect to this server

openai.api_key = os.getenv("OPENAI_API_KEY")

# Dictionary to store chat history per user session
conversation_histories = {}

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_id = data.get("user_id", "default")  # Unique ID for the user session
    user_message = data.get("message", "")

    if user_id not in conversation_histories:
        conversation_histories[user_id] = [{"role": "system", "content": "You are a helpful AI."}]

    # Add user message to history
    conversation_histories[user_id].append({"role": "user", "content": user_message})

    try:
        # Send full conversation history to OpenAI
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation_histories[user_id],  # Send full history
            temperature=0.7
        )

        # Get AI response
        ai_response = response.choices[0].message.content

        # Add AI response to history
        conversation_histories[user_id].append({"role": "assistant", "content": ai_response})

        return jsonify({"response": ai_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
