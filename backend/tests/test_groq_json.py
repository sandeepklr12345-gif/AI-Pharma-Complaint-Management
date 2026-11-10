"""call_groq_json must survive the messy output small models produce."""
import pytest

from app.services import groq_client


@pytest.fixture
def reply(monkeypatch):
    def _set(text: str):
        monkeypatch.setattr(groq_client, "call_groq", lambda system, user, temperature=0.2: text)
    return _set


def test_plain_json(reply):
    reply('{"risk_level": "High"}')
    assert groq_client.call_groq_json("sys", "user") == {"risk_level": "High"}


def test_markdown_fences_are_stripped(reply):
    reply('```json\n{"product_name": "Paracetamol 500"}\n```')
    assert groq_client.call_groq_json("sys", "user") == {"product_name": "Paracetamol 500"}


def test_stray_text_around_json_is_ignored(reply):
    reply('Sure! Here is the result:\n{"batch_number": "B-17"}\nHope that helps.')
    assert groq_client.call_groq_json("sys", "user") == {"batch_number": "B-17"}


def test_unparseable_output_returns_error_marker(reply):
    reply("I cannot do that.")
    result = groq_client.call_groq_json("sys", "user")
    assert result["_parse_error"] is True
    assert result["_raw"] == "I cannot do that."


def test_json_only_instruction_is_appended(monkeypatch):
    seen = {}

    def fake(system, user, temperature=0.2):
        seen["system"] = system
        return "{}"

    monkeypatch.setattr(groq_client, "call_groq", fake)
    groq_client.call_groq_json("Extract fields.", "text")
    assert seen["system"].startswith("Extract fields.")
    assert "ONLY a valid JSON object" in seen["system"]
