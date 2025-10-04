import streamlit as st
import requests
from geopy.geocoders import Nominatim
from src.components.utils import log_message
from requests.exceptions import RequestException

def get_weather(location):
    """Fetches weather data for the given location using Open-Meteo API."""
    geolocator = Nominatim(user_agent="jp_travel_chatbot")
    loc = geolocator.geocode(location, language="en")
    log_message(f"Geocoded location: {loc}")
    if not loc:
        log_message(f"Geocode failed for {location}")
        return {"error": "Location not found"}
    
    lat, lon = loc.latitude, loc.longitude
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m&timezone=Asia%2FTokyo"
    try:
        response = requests.get(url, timeout=10)
        log_message(f"Weather API response status: {response.status_code}")
        if response.status_code != 200:
            return {"error": "API request failed"}
        return response.json()
    except RequestException as e:
        log_message(f"Weather API error: {e}")
        return {"error": "API request exception"}

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
