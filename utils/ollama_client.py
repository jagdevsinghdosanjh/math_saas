import requests
from utils.config import OLLAMA_URL, OLLAMA_MODEL_MATH, OLLAMA_MODEL_SUMMARY

def _call_ollama(model: str, prompt: str) -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    resp = requests.post(OLLAMA_URL, json=payload)
    resp.raise_for_status()
    return resp.json().get("response", "").strip()

def ask_ollama_math(prompt: str) -> str:
    return _call_ollama(OLLAMA_MODEL_MATH, prompt)

def ask_ollama_summary(prompt: str) -> str:
    return _call_ollama(OLLAMA_MODEL_SUMMARY, prompt)