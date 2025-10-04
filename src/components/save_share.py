import urllib.parse
import streamlit as st
from src.components.utils import log_message
from src.components.parsers import sanitize_text

def save_and_share(response):
    """Allows saving and sharing responses."""
    log_message(f"Saving/sharing: {response}")
    if st.button("Bookmark"):
        if 'bookmarks' not in st.session_state:
            st.session_state.bookmarks = []
        st.session_state.bookmarks.append(sanitize_text(response))
    
    tweet_text = urllib.parse.quote_plus(sanitize_text(response)[:200])
    share_url = f"https://twitter.com/intent/tweet?text={tweet_text}"
    st.markdown(f"[Share on Twitter]({share_url})")
