import streamlit as st
from groq import Groq
import os
from src.components.utils import log_message

def get_ai_suggestion(prompt):
    """Gets a suggestion from Groq LLM based on the prompt."""
    client = Groq(api_key=os.environ.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY"))
    log_message(f"Calling LLM with prompt: {prompt}")
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant that suggests activities based on weather and theme in Japanese."},
            {"role": "user", "content": prompt},
        ],
        model="llama-3.1-8b-instant",
    )
    log_message(f"Chat completion response: {chat_completion}")
    return chat_completion.choices[0].message.content
