# services/summary.py

import json
from utils.ollama_client import ask_ollama_summary


def summarize_chapter(text: str) -> str:
    """
    Summarize a chapter into clear, structured notes.
    Uses the new /api/generate summary engine.
    Ensures JSON-safe output and prevents blank UI.
    """

    max_chars = 4000
    if len(text) > max_chars:
        text = text[:max_chars]

    raw = ask_ollama_summary(text)

    # Try JSON parsing safely
    try:
        data = json.loads(raw)
        if isinstance(data, dict) and "summary" in data:
            return data["summary"].strip()
    except json.JSONDecodeError:
        pass
    except Exception:
        pass

    return raw.strip()
