import streamlit as st
from src.components.utils import log_message
from src.components.parsers import sanitize_text

def display_chat_history():
    """Displays the chat history from session state."""
    log_message(f"Current chat history: {st.session_state.messages}")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(sanitize_text(message["content"]))
