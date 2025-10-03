import streamlit as st
from src.components.utils import log_message

def get_user_preferences():
    """Manages user preferences."""
    if 'preferences' not in st.session_state:
        st.session_state.preferences = {}
    
    prefs = st.multiselect("Preferences", ["Family-Friendly", "Romantic", "Adventure"])
    st.session_state.preferences['prefs'] = prefs
    log_message(f"User preferences: {st.session_state.preferences}")
    return st.session_state.preferences
