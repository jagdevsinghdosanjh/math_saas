import requests
import json
from utils.config import (
    OLLAMA_URL,
    OLLAMA_MODEL_MATH,
    OLLAMA_MODEL_SUMMARY,
    USE_OLLAMA
)

# ============================================================
# INTERNAL LOW-LEVEL CALL
# ============================================================

def _call_ollama(model: str, prompt: str) -> str:
    """
    Low-level Ollama API call using /api/chat.
    Includes full debug logging and safe error handling.
    """

    if not USE_OLLAMA:
        return "Ollama disabled in config.py"

    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ]
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
            timeout=30  # Cloudflare-safe
        )

        print(f"STATUS CODE: {response.status_code}")

        # Raise HTTP errors
        response.raise_for_status()

        # Parse JSON safely
        data = response.json()
        print("RAW RESPONSE:", json.dumps(data, indent=2)[:500])

        # Extract content
        if "message" in data and "content" in data["message"]:
            return data["message"]["content"].strip()

        if "response" in data:
            return data["response"].strip()

        return "Error: Unexpected Ollama response format"

    except requests.exceptions.Timeout:
        return "Error: Ollama request timed out (30s). Server may be slow or overloaded."

    except requests.exceptions.ConnectionError as e:
        return f"Connection Error: {str(e)}"

    except requests.exceptions.HTTPError as e:
        return f"HTTP Error: {str(e)}"

    except json.JSONDecodeError:
        return "Error: Invalid JSON received from Ollama."

    except Exception as e:
        return f"Unexpected Error: {str(e)}"


# ============================================================
# PUBLIC FUNCTIONS
# ============================================================

def ask_ollama_math(prompt: str) -> str:
    """Use math model"""
    return _call_ollama(OLLAMA_MODEL_MATH, prompt)


def ask_ollama_summary(prompt: str) -> str:
    """Use summary model"""
    return _call_ollama(OLLAMA_MODEL_SUMMARY, prompt)


# import requests
# from utils.config import OLLAMA_URL, OLLAMA_MODEL_MATH, OLLAMA_MODEL_SUMMARY


# def _call_ollama(model: str, prompt: str) -> str:
#     """
#     Calls Ollama using the /api/chat endpoint.
#     Returns a clean string response.
#     """

#     payload = {
#         "model": model,
#         "prompt": prompt,
#         "stream": False
#     }

#     try:
#         resp = requests.post(OLLAMA_URL, json=payload, timeout=120)
#         resp.raise_for_status()

#         data = resp.json()
#         return (data.get("response") or "").strip()

#     except Exception as e:
#         return f"Ollama error: {str(e)}"


# def ask_ollama_math(prompt: str) -> str:
#     return _call_ollama(OLLAMA_MODEL_MATH, prompt)


# def ask_ollama_summary(prompt: str) -> str:
#     return _call_ollama(OLLAMA_MODEL_SUMMARY, prompt)
