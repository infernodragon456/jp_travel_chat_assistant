import json
import streamlit as st
from groq import Groq
import os
from src.components.utils import log_message
from src.components.parsers import (
    ActivitiesResponse,
    LocationExtraction,
    parse_model_or_raise,
)

def _get_client() -> Groq:
    return Groq(api_key=os.environ.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY"))


def get_ai_text(prompt: str) -> str:
    """Low-level helper to get raw assistant content as text."""
    client = _get_client()
    log_message(f"Calling LLM with prompt: {prompt}")
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant that suggests activities based on weather and theme in Japanese. "
                    "Use Japanese characters and avoid Romaji."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        model="llama-3.1-8b-instant",
        temperature=0.4,
    )
    content = chat_completion.choices[0].message.content or ""
    log_message(f"Chat completion received: {content[:300]}...")
    return content


def get_location_structured(user_query: str) -> LocationExtraction:
    """Ask the model to return a strict JSON object with location extraction."""
    instruction = (
        "Extract the location name from the Japanese query. If no clear location, set location to null. "
        "Return JSON only that matches this schema strictly: {\"location\": string|null}. "
        "Do not include any additional keys or commentary."
    )
    prompt = f"{instruction}\n\nQuery: {user_query}\n\nReturn JSON:"
    text = get_ai_text(prompt)
    return parse_model_or_raise(text, LocationExtraction)


def get_activities_structured(theme: str, preferences_text: str, weather_text: str, user_query: str, location: str | None = None) -> ActivitiesResponse:
    """Ask the model for activities in a strict JSON schema and parse it."""
    schema_hint = json.dumps(
        {
            "message": "string (assistant summary in Japanese)",
            "activities": [
                {
                    "name": "string",
                    "description": "string",
                    "rating": 4.5,
                    "image": "https://example.com/image.jpg",
                    "link": "https://example.com",
                }
            ],
        },
        ensure_ascii=False,
    )
    loc_clause = f" All activities MUST be located in or near '{location}'." if location else ""
    instruction = (
        "Provide exactly 3 Japanese activity suggestions as strict JSON. "
        "The JSON MUST match this shape and nothing else. Do NOT include markdown, backticks, or code fences. "
        "Use natural, fluent Japanese with appropriate place names." + loc_clause
    )
    user = (
        f"Theme: {theme}. Preferences: {preferences_text}. Weather: {weather_text}. "
        f"User query: {user_query}."
    )
    prompt = f"{instruction}\n\nSchema example (values illustrative):\n{schema_hint}\n\nReturn JSON now for: {user}"
    text = get_ai_text(prompt)
    return parse_model_or_raise(text, ActivitiesResponse)


# Backward-compatible function name used by main.py
def get_ai_suggestion(prompt: str) -> str:
    try:
        return get_ai_text(prompt)
    except Exception as e:
        log_message(f"LLM error: {e}")
        return ""
