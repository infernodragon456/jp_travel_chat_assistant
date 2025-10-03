import streamlit as st
from groq import Groq
import os

def get_ai_suggestion(prompt):
    """Gets a suggestion from Groq LLM based on the prompt."""
    client = Groq(api_key=os.environ.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY"))
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant that suggests activities based on weather and theme in Japanese."},
            {"role": "user", "content": prompt},
        ],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content
