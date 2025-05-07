import os
import requests
from flask import Flask, redirect, url_for, render_template, request, jsonify
from dotenv import load_dotenv
from functions import (
    initialize_conversation,
    get_groq_completions
)

# Load environment variables from .env file
load_dotenv()

# Get Groq API Key from .env file
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("❌ ERROR: Groq API Key is missing. Add it to the '.env' file as 'GROQ_API_KEY'.")

# Groq API Configuration
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

app = Flask(__name__)

conversation_bot = []
conversation = initialize_conversation()

@app.route("/")
def default_func():
    """Displays the chatbot UI."""
    return render_template("conversation_bot.html", name_xyz=conversation_bot)

@app.route("/end_conversation", methods=['POST', 'GET'])
def end_conv():
    """Resets conversation when the user ends the chat."""
    global conversation_bot, conversation
    conversation_bot = []
    conversation = initialize_conversation()
    introduction = get_groq_completions(conversation)
    conversation_bot.append({'bot': introduction})
    return redirect(url_for('default_func'))

@app.route("/set_category", methods=["GET"])
def set_category():
    """Handles category updates."""
    category = request.args.get("category", "default")
    return jsonify({"category": category, "message": "Category updated successfully"})

@app.route("/conversation", methods=['POST'])
def invite():
    """Handles user messages and chatbot responses."""
    global conversation_bot, conversation
    user_input = request.form.get("user_input_message", "").strip()

    if not user_input:
        return redirect(url_for('default_func'))

    # Moderation Check (Replace with actual moderation logic if needed)
    if "hate" in user_input.lower():
        return redirect(url_for('end_conv'))

    conversation.append({"role": "user", "content": user_input})
    conversation_bot.append({'user': user_input})

    # Fetch AI Response from Groq
    response_assistant = get_groq_completions(conversation)
    conversation.append({"role": "assistant", "content": response_assistant})
    conversation_bot.append({'bot': response_assistant})

    return redirect(url_for('default_func'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
