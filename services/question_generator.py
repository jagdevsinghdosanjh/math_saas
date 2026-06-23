import json
from utils.model_router import ask_model


def generate_questions(chapter: str, count: int = 10) -> list:
    """
    Generate exam-style math questions using the intelligent model router.
    Ensures:
    - No Cloudflare 524 timeouts
    - llama3 used for long prompts
    - JSON output is validated and repaired if needed
    """

    # Safety: trim extremely long chapter text
    max_chars = 3000
    if len(chapter) > max_chars:
        chapter = chapter[:max_chars]

    prompt = f"""
You are a math question generator.

Chapter/topic: {chapter}

Generate {count} high-quality math questions of mixed difficulty.
Return STRICTLY valid JSON (no commentary, no markdown), in this format:

[
  {{"question": "...", "answer": "...", "difficulty": "easy|medium|hard"}},
  ...
]
"""

    # Use the new router (NOT ask_model_math)
    raw = ask_model(prompt, task="questions")

    # Try to parse JSON directly
    try:
        data = json.loads(raw)
        if isinstance(data, list):
            return data
    except Exception:
        pass

    # Attempt to repair common JSON issues
    repaired = _attempt_json_repair(raw)
    if repaired:
        return repaired

    # Final fallback: return raw text as a single question
    return [{
        "question": raw.strip(),
        "answer": "",
        "difficulty": "unknown"
    }]


def _attempt_json_repair(text: str) -> list | None:
    """
    Attempts to fix common JSON issues:
    - trailing commas
    - missing brackets
    - extra text before/after JSON
    - single quotes instead of double quotes
    """

    try:
        # Extract JSON-like content
        start = text.find("[")
        end = text.rfind("]") + 1
        if start != -1 and end != -1:
            snippet = text[start:end]

            # Replace single quotes with double quotes
            snippet = snippet.replace("'", '"')

            # Remove trailing commas
            snippet = snippet.replace(",]", "]")

            data = json.loads(snippet)
            if isinstance(data, list):
                return data
    except Exception:
        return None

    return None

# import json
# from utils.model_router import ask_model

# def generate_questions(chapter: str, count: int = 10) -> list:
#     prompt = f"""
#     You are a math question generator.

#     Chapter/topic: {chapter}
#     Generate {count} questions of mixed difficulty.
#     Return STRICTLY valid JSON (no extra text), in this format:

#     [
#       {{"question": "...", "answer": "...", "difficulty": "easy|medium|hard"}},
#       ...
#     ]
#     """

#     raw = ask_model_math(prompt, task="questions")

#     try:
#         data = json.loads(raw)
#         if isinstance(data, list):
#             return data
#     except Exception:
#         pass

#     return [{"question": raw, "answer": "", "difficulty": "unknown"}]