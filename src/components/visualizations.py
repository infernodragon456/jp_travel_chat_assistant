import streamlit as st
import altair as alt
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
import pandas as pd
from src.components.utils import log_message

def render_weather_visualization(weather_data, location):
    """Renders interactive weather chart and map."""
    log_message(f"Rendering visualization for {location}: {weather_data}")
    
    # Weather Chart
    if 'hourly' in weather_data:
        df = pd.DataFrame({
            'time': weather_data['hourly']['time'],
            'temperature': weather_data['hourly']['temperature_2m']
        })
        chart = alt.Chart(df).mark_line().encode(
            x='time:T',
            y='temperature:Q'
        ).properties(title=f"Temperature Trend in {location}")
        st.altair_chart(chart, use_container_width=True)
    
    # Map
    geolocator = Nominatim(user_agent="jp_travel_chatbot")
    try:
        loc = geolocator.geocode(location)
    except Exception as e:
        log_message(f"Geocode error in visualization: {e}")
        loc = None
    if loc:
        m = folium.Map(location=[loc.latitude, loc.longitude], zoom_start=12)
        folium.Marker([loc.latitude, loc.longitude], popup=location).add_to(m)
        folium_static(m)
