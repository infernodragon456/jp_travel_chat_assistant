import streamlit as st
from src.components.utils import log_message

def process_voice_command(text):
    """Processes voice commands for navigation."""
    log_message(f"Voice command: {text}")
    if "show weather" in text.lower():
        st.write("Showing weather...")
        # Trigger weather render
    elif "next activity" in text.lower():
        st.write("Next activity...")
        # Logic for next suggestion
    return text  # Return for main processing
