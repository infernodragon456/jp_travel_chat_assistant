import streamlit as st
from datetime import date
from src.components.utils import log_message

def render_challenge(theme):
    """Renders daily/weekly challenges."""
    today = date.today()
    challenge = f"Daily Challenge ({today}): Explore a {theme} spot in rainy weather!"
    st.write(challenge)
    log_message(f"Rendered challenge: {challenge}")
