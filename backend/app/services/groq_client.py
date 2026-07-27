import json
import re
from groq import Groq

from app.config import settings

client = Groq(api_key=settings.groq_api_key)


def call_groq(system_prompt: str, user_prompt: str, temperature: float = 0.2) -> str:
    """Single chat completion call. Kept low temperature for consistent extraction."""
    response = client.chat.completions.create(
        model=settings.groq_model,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content


def call_groq_json(system_prompt: str, user_prompt: str) -> dict:
    """
    gemma2-9b-it doesn't have a strict JSON mode like larger models,
    so we (a) instruct it hard to return ONLY JSON, and (b) defensively
    strip any markdown fences or stray text the model adds anyway.
    """
    strict_system = (
        system_prompt
        + "\n\nYou must respond with ONLY a valid JSON object. "
          "No markdown, no code fences, no explanation before or after."
    )
    raw = call_groq(strict_system, user_prompt)

    # Strip ```json fences if the model adds them despite instructions
    cleaned = re.sub(r"^```(json)?|```$", "", raw.strip(), flags=re.MULTILINE).strip()

    # Fallback: grab the first {...} block if there's still stray text
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    json_str = match.group(0) if match else cleaned

    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        # Return a shape the caller can detect and handle gracefully
        return {"_parse_error": True, "_raw": raw}
