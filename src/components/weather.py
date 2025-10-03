import streamlit as st
import requests
from geopy.geocoders import Nominatim
from src.components.utils import log_message

def get_weather(location):
    """Fetches weather data for the given location using Open-Meteo API."""
    geolocator = Nominatim(user_agent="jp_travel_chatbot")
    loc = geolocator.geocode(location, language="en")
    log_message(f"Geocoded location: {loc}")
    if not loc:
        return {"error": "Location not found"}
    
    lat, lon = loc.latitude, loc.longitude
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m&timezone=Asia%2FTokyo"
    response = requests.get(url)
    log_message(f"Weather API response status: {response.status_code}")
    return response.json()

def render_weather_component():
    """Renders the weather information for the last location in session state."""
    if 'last_location' in st.session_state:
        weather_data = get_weather(st.session_state.last_location)
        if "error" not in weather_data:
            current = weather_data['current_weather']
            st.subheader(f"Current Weather in {st.session_state.last_location}")
            st.write(f"Temperature: {current['temperature']}°C")
            st.write(f"Wind Speed: {current['windspeed']} km/h")
            st.write(f"Weather Code: {current['weathercode']}")
        else:
            st.write("Weather data not available.")
