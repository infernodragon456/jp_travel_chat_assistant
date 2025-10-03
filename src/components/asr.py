import streamlit as st
from streamlit_mic_recorder import mic_recorder
import whisper

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
            
            # Load Whisper model and transcribe
            model = whisper.load_model("base")
            result = model.transcribe(temp_file, language="ja")
            text = result["text"]
            
            # Store transcribed text in session state for main.py to process
            st.session_state.voice_text = text
            st.write(f"Transcribed: {text}")
