import streamlit as st
import requests
from src.components.utils import log_message

def get_external_info(location):
    """Fetches external info like hotels/restaurants."""
    log_message(f"Fetching external info for {location}")
    # Mock API call (e.g., to TripAdvisor or similar free API)
    st.markdown("[Tourism Info](https://www.japan.travel/)")
    st.markdown(f"[Google Maps for {location}](https://maps.google.com/?q={location})")
