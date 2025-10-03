from googletrans import Translator
import streamlit as st
from src.components.utils import log_message

translator = Translator()

def translate_text(text, lang='ja'):
    """Translates text to the target language."""
    log_message(f"Translating: {text} to {lang}")
    return translator.translate(text, dest=lang).text

def render_language_selector():
    """Renders language toggle."""
    lang = st.selectbox("Language", ["Japanese", "English"], key="lang")
    return 'ja' if lang == "Japanese" else 'en'
