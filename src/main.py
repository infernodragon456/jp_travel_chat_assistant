import streamlit as st
import sys
import os

# Add project root to sys.path for absolute imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.components.chat import display_chat_history
from src.components.weather import render_weather_component
from src.components.asr import render_voice_input
from src.components.tts import render_tts_output
from src.components.llm import (
    get_ai_suggestion,
    get_location_structured,
    get_activities_structured,
)
from src.components.weather import get_weather
from src.components.tts import generate_tts
from src.components.utils import log_message
from src.components.parsers import sanitize_text
import re
import streamlit_shadcn_ui as ui
from datetime import datetime

from src.components.visualizations import render_weather_visualization
from src.components.activity_cards import render_activity_card
from src.components.location_services import get_user_location
from src.components.itinerary import build_itinerary
from src.components.personalization import get_user_preferences
from src.components.voice_navigation import process_voice_command
from src.components.external_integrations import get_external_info
from src.components.save_share import save_and_share
from src.components.challenges import render_challenge

st.set_page_config(page_title="Japanese Weather Travel Chatbot", layout="wide")

ui.subheader("Japanese Weather Travel Chatbot")

with st.sidebar:
    ui.subheader("Settings")
    theme = st.selectbox("Theme", ["Travel", "Outings", "Fashion", "Sports"], key="theme")

# Initialize session state for messages if not present
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.container():
    # Top input bar using shadcn ui
    ui.card(lambda: (
        ui.input("Type your message here (or use voice)", key="top_text_input"),
        ui.button("Send", key="send_btn", variant="primary"),
    ))
    # Assign from ui input and button
    prompt = st.session_state.get("top_text_input")
    send_clicked = bool(st.session_state.get("send_btn"))
    # Voice input under the bar
    render_voice_input()

process_input = False
if send_clicked and prompt:
    process_input = True

# Check for voice input
if 'voice_text' in st.session_state and st.session_state.voice_text:
    prompt = st.session_state.voice_text
    del st.session_state.voice_text
    process_input = True

# Process the input if available
if process_input:
    prompt = process_voice_command(prompt)  # Process for commands
    st.session_state.messages.append({"role": "user", "content": prompt})
    log_message(f"User input: {prompt}")

    # Extract location using structured LLM output
    try:
        loc_struct = get_location_structured(prompt)
        location = (loc_struct.location or '').strip()
        location = location if location else 'NONE'
    except Exception as e:
        log_message(f"Location extraction parse error: {e}")
        location = 'NONE'
    log_message(f"Extracted location: {location}")

    if location != 'NONE':
        # Fetch more detailed weather (update get_weather to include hourly)
        weather_data = get_weather(location)  # Assume updated to include hourly
        log_message(f"Weather data: {weather_data}")
        if "error" not in weather_data:
            current = weather_data['current_weather']
            weather_str = f"Current temperature: {current['temperature']}°C, Weather code: {current['weathercode']}"
            st.session_state.last_location = location
            render_weather_visualization(weather_data, location)
        else:
            weather_str = "Weather data not available."
    else:
        weather_str = "No weather information available."

    # Generate structured activities and assistant message
    try:
        prefs_obj = get_user_preferences()
        activities_struct = get_activities_structured(
            theme=theme,
            preferences_text=str(prefs_obj),
            weather_text=weather_str,
            user_query=prompt,
            location=location if location != 'NONE' else None,
        )
        response = activities_struct.message or ""
        # Convert HttpUrl to strings for rendering safely
        activities = [
            a.model_dump(mode="json")  # ensure URLs are serialized as strings
            for a in activities_struct.activities
        ]
    except Exception as e:
        log_message(f"Activities parsing error: {e}")
        # Fallback: plain text response
        fallback_prompt = f"{theme} {prompt} {weather_str}"
        response = get_ai_suggestion(fallback_prompt)
        activities = []

    # Clean response for TTS and safe display
    clean_response = sanitize_text(response)

    st.session_state.messages.append({"role": "assistant", "content": clean_response})

    # Structured UI layout
    try:
        tabs = st.tabs(["Suggestions", "Itinerary", "Map & Weather", "Bookmarks", "Extras"])

        with tabs[0]:
            ui.subheader("Suggested Activities")
            # Metrics row
            col_a, col_b, col_c = st.columns(3)
            loc_label = location if location != 'NONE' else '—'
            temp_label = f"{current['temperature']}°C" if location != 'NONE' and "current_weather" in weather_data else '—'
            with col_a:
                st.metric("Location", loc_label)
            with col_b:
                st.metric("Temperature", temp_label)
            with col_c:
                st.metric("Activities", len(activities))
            if activities:
                for act in activities:
                    render_activity_card(act)
            else:
                st.info("No activities available. Try refining your request.")
            save_and_share(clean_response)

        with tabs[1]:
            ui.subheader("Build Your Itinerary")
            if activities:
                build_itinerary(activities)
            else:
                st.write("Add some activities first from Suggestions.")

        with tabs[2]:
            ui.subheader("Map & Weather")
            if location != 'NONE':
                col_left, col_right = st.columns([2, 1])
                with col_left:
                    render_weather_visualization(weather_data if location != 'NONE' else {}, location)
                with col_right:
                    st.subheader(f"Current Weather in {location}")
                    if "error" not in weather_data:
                        cw = weather_data.get('current_weather', {})
                        if cw:
                            st.metric("Temp", f"{cw.get('temperature', '—')}°C")
                            st.metric("Wind", f"{cw.get('windspeed', '—')} km/h")
                            st.metric("Code", f"{cw.get('weathercode', '—')}")
                    else:
                        st.write("Weather data not available.")
            else:
                st.write("No location found.")

        with tabs[3]:
            ui.subheader("Bookmarks")
            bmarks = st.session_state.get('bookmarked_activities', [])
            if bmarks:
                # Summary table
                try:
                    table_rows = [{
                        'Name': b.get('name', ''),
                        'Rating': b.get('rating', ''),
                        'Link': b.get('link', ''),
                    } for b in bmarks]
                    st.dataframe(table_rows, use_container_width=True)
                except Exception:
                    pass
                # Cards
                for b in bmarks:
                    render_activity_card(b)
            else:
                st.write("No bookmarks yet.")

        with tabs[4]:
            ui.subheader("Extras")
            render_challenge(theme)
            get_external_info(location)
    except Exception as e:
        log_message(f"Error in rendering features: {e}")
        st.error("An error occurred while rendering additional features.")

    # Generate TTS with cleaned text
    audio_file = generate_tts(clean_response)
    if audio_file:
        log_message(f"TTS file generated: {audio_file}")
        st.session_state.tts_file = audio_file
    else:
        st.warning("TTS generation failed.")

# Display chat history
display_chat_history()

# Render TTS component
render_tts_output()

# Clear send state after processing
if process_input:
    st.session_state["top_text_input"] = ""
    st.session_state["send_btn"] = False
