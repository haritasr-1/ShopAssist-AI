import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Groq API Configuration
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("❌ ERROR: Groq API Key is missing. Add it to the '.env' file as 'GROQ_API_KEY'.")

# Function to send requests to Groq API
def get_groq_completions(messages):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192",  # Use "mixtral-8x7b-32768" if needed
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 200
    }
    try:
        response = requests.post(GROQ_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response from AI.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Groq API Error: {e}")
        return "Sorry, I'm having trouble processing your request right now."

# Function to initialize a new conversation
def initialize_conversation():
    return [
        {"role": "system", "content": "You are an AI assistant that provides general assistance based on user queries. Respond accordingly to different topics like fashion, electronics, health, and more."}
    ]

# Function to initialize recommendations conversation
def initialize_conv_reco(validated_reco):
    return [
        {"role": "system", "content": "You are an AI assistant that provides recommendations based on user preferences."},
        {"role": "assistant", "content": validated_reco}
    ]

# Function to check user intent confirmation
def intent_confirmation_layer(response):
    messages = [
        {"role": "system", "content": "Does this response confirm the user's intent? Reply with 'Yes' or 'No'."},
        {"role": "user", "content": response}
    ]
    return get_groq_completions(messages)

# Function to compare products with user preferences
def compare_products_with_user(user_preferences):
    messages = [
        {"role": "system", "content": "Based on the user's preferences, compare products and suggest top 3 options."},
        {"role": "user", "content": user_preferences}
    ]
    return get_groq_completions(messages)

# Function to validate recommendations
def recommendation_validation(recommendations):
    messages = [
        {"role": "system", "content": "Validate the recommendations and ensure they meet user needs."},
        {"role": "user", "content": recommendations}
    ]
    return get_groq_completions(messages)

# Function to generate user requirement string
def get_user_requirement_string(response_assistant):
    messages = [
        {"role": "system", "content": "Extract key user requirements from the response."},
        {"role": "user", "content": response_assistant}
    ]
    return get_groq_completions(messages)

# Function to get chat completions (Replaces OpenAI)
def get_chat_completions_func_calling(response, validate=False):
    messages = [{"role": "user", "content": response}]
    if validate:
        messages.insert(0, {"role": "system", "content": "Validate the user request and provide recommendations."})
    return get_groq_completions(messages)
