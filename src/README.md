# Japanese Weather Travel Chatbot

## Overview
This is a Streamlit-based chatbot that supports Japanese voice input using Whisper, integrates with the free Open-Meteo weather API, and uses Groq LLM for generating activity suggestions based on weather and selected theme (e.g., travel, outings).

## Setup
1. Install dependencies: `pip install -r src/requirements.txt`
2. Set `GROQ_API_KEY` in environment variables or in `.streamlit/secrets.toml`.
3. Run the app: `streamlit run src/main.py`

## Deployment
- Push the repository to GitHub (public).
- Deploy on Streamlit Community Cloud by connecting the repo and setting the `GROQ_API_KEY` secret.
- Alternative: Use Render.com free tier.

## Japanese Input/Voice Features
- Voice input is handled via browser microphone with Whisper transcription for Japanese.
- Responses are in Japanese with TTS audio playback.

## Example Prompt
"東京で明日おすすめのアクティビティは？" (What's a recommended activity in Tokyo tomorrow?)

## Demo Usage
- Select a theme in the sidebar.
- Use voice input or type a query in Japanese.
- The bot fetches weather, generates suggestions, and plays audio response.

For a working demo, deploy to Streamlit Cloud or run locally and record a video.

## New Features
- Interactive weather visualizations and maps
- Rich activity cards with images and links
- Auto/manual location detection
- Multilingual support (Japanese/English)
- Itinerary building and export
- User preference saving
- Voice command navigation
- External service integrations
- Save/share functionality
- Daily challenges
