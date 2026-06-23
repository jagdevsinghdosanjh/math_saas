# services/solver.py

import json
from utils.model_router import ask_model


def solve_stepwise(question: str) -> dict:
    """
    Step-by-step math solver using the intelligent model router.
    - Uses deepseek-r1 only for short prompts
    - Falls back to llama3 for longer ones (avoids Cloudflare 524)
    - Ensures JSON output is parsed or safely wrapped
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

    raw = ask_model(prompt, task="math")

    # Try direct JSON parse
    try:
        data = json.loads(raw)
        if isinstance(data, dict):
            return data
    except Exception:
        pass

    # Try to repair common JSON issues
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

# # from utils.ollama_client import ask_ollama
# from utils.ollama_client import ask_ollama_math
# import json

# def solve_stepwise(question: str):
#     prompt = f"""
#     Solve this math problem step-by-step.
#     Return STRICT JSON:
#     {{
#       "steps": ["step 1 ...", "step 2 ..."],
#       "final_answer": "..."
#     }}

#     Problem: {question}
#     """

#     raw = ask_ollama_math(prompt)

#     try:
#         data = json.loads(raw)
#         if isinstance(data, dict):
#             return data
#     except:
#         pass

#     return {
#         "steps": [raw],
#         "final_answer": ""
#     }


# def solve_stepwise(question: str):
#     prompt = f"""
#     Solve this math problem step-by-step.
#     Return answer in JSON:
#     {{
#       "steps": ["...", "..."],
#       "final_answer": "..."
#     }}

#     Problem: {question}
#     """

#     response = ask_ollama(prompt)
#     return response
