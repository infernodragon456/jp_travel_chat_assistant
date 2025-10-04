import json
import re
from typing import Optional, List

import bleach
from pydantic import BaseModel, HttpUrl, ValidationError, field_validator


class Activity(BaseModel):
    name: str
    description: str
    rating: Optional[float] = None
    image: Optional[HttpUrl] = None
    link: Optional[HttpUrl] = None

    @field_validator("rating")
    @classmethod
    def clamp_rating(cls, value: Optional[float]) -> Optional[float]:
        if value is None:
            return value
        try:
            # Ensure rating is within 0-5 range
            value = float(value)
        except Exception:
            return None
        if value < 0:
            return 0.0
        if value > 5:
            return 5.0
        return value


class ActivitiesResponse(BaseModel):
    message: Optional[str] = None
    activities: List[Activity]


class LocationExtraction(BaseModel):
    location: Optional[str] = None


def _extract_json_substring(text: str) -> Optional[str]:
    """Extracts the first JSON object or array substring from text.

    Handles cases where the model returns ```json code fences or stray prose around JSON.
    """
    if not text:
        return None
    # Strip code fences if present
    fenced = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text, flags=re.IGNORECASE)
    if fenced:
        candidate = fenced.group(1).strip()
        if candidate:
            return candidate

    # Fallback: find first top-level JSON object or array using a simple stack parser
    start_idx = None
    stack = []
    for idx, ch in enumerate(text):
        if ch in "[{":
            if not stack:
                start_idx = idx
            stack.append(ch)
        elif ch in "]}":
            if stack:
                stack.pop()
                if not stack and start_idx is not None:
                    return text[start_idx : idx + 1]
    return None


def parse_model_or_raise(text: str, model_cls: type[BaseModel]) -> BaseModel:
    """Parse text into the given Pydantic model, raising ValidationError on failure.

    - Extracts JSON from common wrappers
    - Attempts direct json.loads first, then extracted substring
    """
    last_error: Optional[Exception] = None
    candidates = [text]
    extracted = _extract_json_substring(text)
    if extracted and extracted not in candidates:
        candidates.append(extracted)

    for candidate in candidates:
        try:
            data = json.loads(candidate)
            return model_cls.model_validate(data)
        except Exception as e:
            last_error = e

    # If nothing worked, raise a validation error with context
    if isinstance(last_error, ValidationError):
        raise last_error
    raise ValidationError.from_exception_data(
        model_cls.__name__,
        [
            {
                "type": "value_error.json_parse",
                "loc": ("__root__",),
                "msg": f"Failed to parse JSON for {model_cls.__name__}: {last_error}",
                "input": text,
            }
        ],
    )


def sanitize_text(text: str) -> str:
    """Sanitize arbitrary text by stripping any HTML and potentially dangerous content.

    We keep plain text by removing all HTML tags and attributes.
    """
    if not isinstance(text, str):
        return ""
    return bleach.clean(text, tags=[], attributes={}, strip=True)


def sanitize_url(url: Optional[str]) -> Optional[str]:
    if not url:
        return url
    cleaned = bleach.clean(url, tags=[], attributes={}, strip=True)
    # Allow only http/https
    if cleaned.startswith("http://") or cleaned.startswith("https://"):
        return cleaned
    return None


