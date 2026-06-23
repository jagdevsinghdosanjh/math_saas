# services/solver.py

import json
from utils.model_router import ask_model


def solve_stepwise(question: str) -> dict:
    """
    Step-by-step math solver using the intelligent model router.
    - Uses deepseek-r1 only for short prompts
    - Uses llama3 for long prompts (avoids Cloudflare 524)
    - Ensures JSON output is parsed or safely repaired
    """

    # Safety: trim very long questions
    max_chars = 1500
    if len(question) > max_chars:
        question = question[:max_chars]

    prompt = f"""
You are an expert math tutor.

Solve this math problem step-by-step.
Return STRICT JSON only (no extra text), in this format:

{{
  "steps": ["step 1 ...", "step 2 ..."],
  "final_answer": "..."
}}

Problem: {question}
"""

    # Use the new router (NOT ask_ollama_math)
    raw = ask_model(prompt, task="math")

    # Try direct JSON parse
    try:
        data = json.loads(raw)
        if isinstance(data, dict):
            return data
    except Exception:
        pass

    # Try to repair malformed JSON
    repaired = _attempt_json_repair(raw)
    if repaired:
        return repaired

    # Final fallback: wrap raw text
    return {
        "steps": [raw.strip()],
        "final_answer": ""
    }


def _attempt_json_repair(text: str) -> dict | None:
    """
    Attempts to fix malformed JSON:
    - extract JSON object
    - replace single quotes
    - remove trailing commas
    """

    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        if start != -1 and end != -1:
            snippet = text[start:end]

            snippet = snippet.replace("'", '"')
            snippet = snippet.replace(",}", "}")

            data = json.loads(snippet)
            if isinstance(data, dict):
                return data
    except Exception:
        return None

    return None
