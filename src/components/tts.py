import streamlit as st
from gtts import gTTS
from src.components.utils import log_message

def generate_tts(text):
    """Generates TTS audio file for the given Japanese text."""
    log_message(f"Generating TTS for text: {text}")
    try:
        tts = gTTS(text, lang='ja')
        file_path = "response.mp3"
        tts.save(file_path)
        log_message(f"TTS saved to: {file_path}")
        return file_path
    except Exception as e:
        log_message(f"TTS error: {e}")
        return None

def render_tts_output():
    """Renders the TTS audio player if available in session state."""
    st.subheader("Voice Response")
    if 'tts_file' in st.session_state:
        st.audio(st.session_state.tts_file, format="audio/mp3", autoplay=True)
