import os
import streamlit as st
from streamlit_mic_recorder import mic_recorder
import whisper
from src.components.utils import log_message


@st.cache_resource(show_spinner=False)
def get_whisper_model():
    return whisper.load_model("base")

def render_voice_input():
    """Renders the voice input component and transcribes Japanese speech."""
    st.subheader("Voice Input (Japanese)")
    audio = mic_recorder(
        start_prompt="🎤 Start recording",
        stop_prompt="🛑 Stop recording",
        key="mic_recorder"
    )
    if audio:
        with st.spinner("Transcribing..."):
            # Save audio to temporary file
            temp_file = "temp_audio.wav"
            with open(temp_file, "wb") as f:
                f.write(audio['bytes'])
            log_message(f"Audio saved to: {temp_file}")
            
            try:
                # Load Whisper model and transcribe
                model = get_whisper_model()
                result = model.transcribe(temp_file, language="ja")
                log_message(f"Transcription result: {result}")
                text = result.get("text", "") or ""
            except Exception as e:
                log_message(f"Transcription error: {e}")
                text = ""
            finally:
                try:
                    os.remove(temp_file)
                except Exception:
                    pass
            
            # Store transcribed text in session state for main.py to process
            st.session_state.voice_text = text
            st.write(f"Transcribed: {text}")
