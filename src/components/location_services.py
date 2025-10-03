import streamlit as st
from geopy.geocoders import Nominatim
from src.components.utils import log_message

def get_user_location():
    """Gets user location via browser or manual input."""
    location = st.text_input("Enter location (or use auto-detect)")
    if st.button("Auto-Detect"):
        # Placeholder for browser geolocation (Streamlit doesn't support directly; use JS component if needed)
        log_message("Auto-detect attempted (placeholder)")
        geolocator = Nominatim(user_agent="jp_travel_chatbot")
        loc = geolocator.geocode("Tokyo")  # Mock; replace with real geo
        location = loc.address if loc else "Tokyo"
    return location
