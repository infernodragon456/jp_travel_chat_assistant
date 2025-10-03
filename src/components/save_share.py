import streamlit as st
from src.components.utils import log_message

def save_and_share(response):
    """Allows saving and sharing responses."""
    log_message(f"Saving/sharing: {response}")
    if st.button("Bookmark"):
        if 'bookmarks' not in st.session_state:
            st.session_state.bookmarks = []
        st.session_state.bookmarks.append(response)
    
    share_url = "https://twitter.com/intent/tweet?text=" + response[:100]
    st.markdown(f"[Share on Twitter]({share_url})")
