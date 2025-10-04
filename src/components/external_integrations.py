import streamlit as st
from src.components.utils import log_message
from src.components.parsers import sanitize_text

def get_external_info(location):
    """Fetches external info like hotels/restaurants."""
    log_message(f"Fetching external info for {location}")
    # Mock API call (e.g., to TripAdvisor or similar free API)
    safe_location = sanitize_text(location or "")
    st.markdown("[Tourism Info](https://www.japan.travel/)")
    st.markdown(f"[Google Maps for {safe_location}](https://maps.google.com/?q={safe_location})")
