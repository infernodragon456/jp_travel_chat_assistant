import streamlit as st
from gtts import gTTS

def generate_tts(text):
    """Generates TTS audio file for the given Japanese text."""
    tts = gTTS(text, lang='ja')
    file_path = "response.mp3"
    tts.save(file_path)
    return file_path

def render_tts_output():
    """Renders the TTS audio player if available in session state."""
    st.subheader("Voice Response")
    if 'tts_file' in st.session_state:
        st.audio(st.session_state.tts_file, format="audio/mp3", autoplay=True)
