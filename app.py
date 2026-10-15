
import os

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from google import genai
from google.genai import types

# =========================================================
# MELOMIND CONFIGURATION
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load API key from backend/.env
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY) if API_KEY else None

MODEL_NAME = "gemini-3.5-flash"

# =========================================================
# CHATBOT PAGE
# =========================================================

@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "chatbot.html")


@app.route("/chatbot.html")
def chatbot_page():
    return send_from_directory(BASE_DIR, "chatbot.html")


# =========================================================
# SERVER STATUS
# =========================================================

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "running",
        "gemini_configured": client is not None
    })


# =========================================================
# GEMINI CHAT API
# =========================================================

@app.route("/api/chat", methods=["POST"])
def chat():

    if client is None:
        return jsonify({
            "error": "Gemini API key is missing. Check your backend/.env file."
        }), 500

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Invalid request. Please send JSON."
        }), 400

    message = data.get("message", "")

    if not isinstance(message, str) or not message.strip():
        return jsonify({
            "error": "Please enter a message."
        }), 400

    history = data.get("history", [])

    if not isinstance(history, list):
        return jsonify({
            "error": "Conversation history must be a list."
        }), 400

    contents = []

    # Include recent conversation history
    for item in history[-20:]:

        if not isinstance(item, dict):
            continue

        role = item.get("role")
        text_content = item.get("text", item.get("content", ""))

        if role == "assistant":
            role = "model"

        if role not in ("user", "model"):
            continue

        if not isinstance(text_content, str):
            continue

        if not text_content.strip():
            continue

        contents.append(
            types.Content(
                role=role,
                parts=[
                    types.Part.from_text(text=text_content.strip())
                ]
            )
        )

    # Add current message
    contents.append(
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=message.strip())
            ]
        )
    )

    # Call Gemini
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=(
                    "You are MeloMind, a friendly and helpful AI "
                    "assistant. Answer clearly, naturally, and "
                    "respectfully. Keep answers easy to understand."
                ),
                temperature=0.7,
                max_output_tokens=2048
            )
        )

        reply = response.text

        if not reply:
            app.logger.error(
                "Gemini returned no text. Finish reason: %s",
                getattr(response.candidates[0], "finish_reason", "unknown")
                if response.candidates else "no candidates"
            )

            return jsonify({
                "error": "Gemini returned an empty response. Please try again."
            }), 502

        return jsonify({
            "reply": reply,
            "response": reply
        })

    except Exception as error:

        # Print the real error in the Flask terminal
        app.logger.exception("Gemini API request failed")

        # Show the error so we can identify the problem
        return jsonify({
            "error": str(error)
        }), 502


# =========================================================
# START SERVER
# =========================================================


@app.route("/robot.png")
def robot_image():
    return send_from_directory(BASE_DIR, "robot.png")


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

