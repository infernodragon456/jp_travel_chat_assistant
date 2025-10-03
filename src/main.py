import streamlit as st

from components.chat import display_chat_history
from components.weather import render_weather_component
from components.asr import render_voice_input
from components.tts import render_tts_output
from components.llm import get_ai_suggestion
from components.weather import get_weather
from components.tts import generate_tts

st.set_page_config(page_title="Japanese Weather Travel Chatbot", layout="wide")

st.title("Japanese Weather Travel Chatbot")

st.sidebar.title("Settings")
theme = st.sidebar.selectbox("Theme", ["Travel", "Outings", "Fashion", "Sports"], key="theme")

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
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Extract location using LLM
    extract_prompt = f"Extract the location name from this Japanese query: {prompt}. If no location, return 'NONE'. Respond only with the location or 'NONE'."
    location = get_ai_suggestion(extract_prompt).strip()

    if location != 'NONE':
        weather_data = get_weather(location)
        if "error" not in weather_data:
            current = weather_data['current_weather']
            weather_str = f"Current temperature: {current['temperature']}°C, Weather code: {current['weathercode']}"
            st.session_state.last_location = location
        else:
            weather_str = "Weather data not available."
    else:
        weather_str = "No weather information available."

    # Generate AI response
    full_prompt = f"Theme: {theme}. Weather: {weather_str}. User query: {prompt}. Provide a helpful response in Japanese suggesting activities or advice based on the theme and weather."
    response = get_ai_suggestion(full_prompt)

    st.session_state.messages.append({"role": "assistant", "content": response})

    # Generate TTS
    audio_file = generate_tts(response)
    st.session_state.tts_file = audio_file

# Display chat history
display_chat_history()

# Render weather and TTS components
render_weather_component()
render_tts_output()
