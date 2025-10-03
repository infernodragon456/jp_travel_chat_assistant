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
from src.components.llm import get_ai_suggestion
from src.components.weather import get_weather
from src.components.tts import generate_tts
from src.components.utils import log_message
import re

from src.components.visualizations import render_weather_visualization
from src.components.activity_cards import render_activity_card
from src.components.location_services import get_user_location
from src.components.multilingual import translate_text, render_language_selector
from src.components.itinerary import build_itinerary
from src.components.personalization import get_user_preferences
from src.components.voice_navigation import process_voice_command
from src.components.external_integrations import get_external_info
from src.components.save_share import save_and_share
from src.components.challenges import render_challenge

st.set_page_config(page_title="Japanese Weather Travel Chatbot", layout="wide")

st.title("Japanese Weather Travel Chatbot")

st.sidebar.title("Settings")
theme = st.sidebar.selectbox("Theme", ["Travel", "Outings", "Fashion", "Sports"], key="theme")
lang = render_language_selector()

# Initialize session state for messages if not present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render voice input component
render_voice_input()

# Text input
prompt = st.chat_input("Type your message here (or use voice)")

process_input = False
if prompt:
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

    # Extract location using LLM
    extract_prompt = f"Extract the location name from this Japanese query: {prompt}. If no location, return 'NONE'. Respond only with the location or 'NONE'."
    location = get_user_location() or get_ai_suggestion(extract_prompt).strip()
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

    # Generate AI response with prefs
    full_prompt = f"Theme: {theme}. Preferences: {get_user_preferences()}. Weather: {weather_str}. User query: {prompt}. Provide a helpful response in Japanese suggesting activities or advice based on the theme and weather. Suggest 3 activities with names, descriptions, ratings, images (use placeholders), and links."
    log_message(f"Full LLM prompt: {full_prompt}")
    response = get_ai_suggestion(full_prompt)
    log_message(f"AI response: {response}")

    # Parse response into activities (mock parsing)
    activities = [{'name': 'Activity 1', 'description': 'Desc', 'rating': 4.5, 'image': 'placeholder.jpg', 'link': 'https://example.com'}] * 3  # Parse from response in real impl

    # Translate if needed
    if lang != 'ja':
        response = translate_text(response, lang)

    # Clean response for TTS
    clean_response = re.sub(r'\*\*(.*?)\*\*', r'\1', response)
    clean_response = re.sub(r'\*(.*?)\*', r'\1', clean_response)

    st.session_state.messages.append({"role": "assistant", "content": response})

    # Render new features
    for act in activities:
        render_activity_card(act)
    build_itinerary(activities)
    get_external_info(location)
    save_and_share(response)
    render_challenge(theme)

    # Generate TTS with cleaned text
    audio_file = generate_tts(clean_response)
    log_message(f"TTS file generated: {audio_file}")
    st.session_state.tts_file = audio_file

# Display chat history
display_chat_history()

# Render weather and TTS components
render_weather_component()
render_tts_output()
