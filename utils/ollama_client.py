# utils/ollama_client.py

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:7b"   # best for math reasoning

def ask_ollama(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()

    data = response.json()
    return data.get("response", "")
