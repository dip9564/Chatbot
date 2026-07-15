import os
import streamlit as st
from google import genai

# from dotenv import load_dotenv
# load_dotenv()

# api_key = os.getenv("GEMINI_API_KEY")

api_key = st.secrets["GEMINI_API_KEY"]

client = genai.Client(api_key=api_key)


def generate_response(user_name,messages, model_name):
    """
    Generate a response using Gemini.
    """
    history = [
        {
            "role": "user",
            "parts": [{"text": f"My name is {user_name}"}]
        }
    ]
    history = [
        {
            "role": "user",
            "parts": [{
                "text": f"""
        
        Your name is Sora.
        You are Dip's personal AI assistant.

        Never introduce yourself as Gemini.
        If someone asks your name, say your name is Sora.
        If someone asks who you are, say you are Sora, Dip's AI assistant.
        If someone asks who created you, say you were created by Dip.
        The user's name is {user_name}. Remember the user's name throughout this conversation and use it naturally when appropriate.
        """
            }]
        }
    ]

    for msg in messages:
        history.append({
            "role": msg["role"],
            "parts": [
                {
                    "text": msg["content"]
                }
            ]
        })
    MODEL_MAP = {
        "💨 Gemini 3.1 Flash Lite": "models/gemini-3.1-flash-lite",
        "🧠 Gemini 3": "models/gemini-3-flash-preview",
        "⚡ Gemini 3.5 Flash": "models/gemini-3.5-flash",
    }
    model = MODEL_MAP.get(model_name, "models/gemini-3.1-flash-lite")
    try:
        response = client.models.generate_content(
            model=model,
            contents=history,
        )

        return response.text

    except Exception as e:
        return (
            "⚠️ The selected model is currently unavailable.\n\n"
            "Please choose another model and try again."
        )