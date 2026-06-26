import requests
import json
from utils.config import (
    OLLAMA_URL,
    OLLAMA_MODEL_MATH,
    OLLAMA_MODEL_SUMMARY,
    USE_OLLAMA
)

# ============================================================
# INTERNAL LOW-LEVEL CALL (FULLY PATCHED)
# ============================================================

def _call_ollama(model: str, prompt: str) -> str:
    """
    Robust Ollama API call.
    Handles:
    - normal JSON
    - streaming JSON (multiple lines)
    - plain text responses
    - safe fallbacks
    """

    if not USE_OLLAMA:
        return "Ollama disabled in config.py"

    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }

    try:
        print("\n================ OLLAMA DEBUG ================")
        print(f"URL: {OLLAMA_URL}")
        print(f"MODEL: {model}")
        print(f"PROMPT: {prompt[:200]}...")
        print("Sending request...")

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=30
        )

        print(f"STATUS CODE: {response.status_code}")
        response.raise_for_status()

        raw_text = response.text.strip()
        print("RAW TEXT RESPONSE:", raw_text[:500])

        # ----------------------------------------------------
        # 1) Try direct JSON
        # ----------------------------------------------------
        try:
            data = response.json()
            print("PARSED JSON:", json.dumps(data, indent=2)[:500])

            if "message" in data and "content" in data["message"]:
                return data["message"]["content"].strip()

            if "response" in data:
                return data["response"].strip()

        except json.JSONDecodeError:
            pass  # Continue to streaming/line-by-line parsing

        # ----------------------------------------------------
        # 2) Try streaming JSON (line-by-line)
        # ----------------------------------------------------
        for line in raw_text.splitlines():
            try:
                data = json.loads(line)

                if "message" in data and "content" in data["message"]:
                    return data["message"]["content"].strip()

                if "response" in data:
                    return data["response"].strip()

            except json.JSONDecodeError:
                continue

        # ----------------------------------------------------
        # 3) Fallback: return raw text
        # ----------------------------------------------------
        return raw_text

    except requests.exceptions.Timeout:
        return "Error: Ollama request timed out (30s)."

    except requests.exceptions.ConnectionError as e:
        return f"Connection Error: {str(e)}"

    except requests.exceptions.HTTPError as e:
        return f"HTTP Error: {str(e)}"

    except Exception as e:
        return f"Unexpected Error: {str(e)}"


# ============================================================
# PUBLIC FUNCTIONS
# ============================================================

def ask_ollama_math(prompt: str) -> str:
    return _call_ollama(OLLAMA_MODEL_MATH, prompt)


def ask_ollama_summary(prompt: str) -> str:
    return _call_ollama(OLLAMA_MODEL_SUMMARY, prompt)