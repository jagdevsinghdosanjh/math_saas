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

# # utils/ollama_client.py

# import requests
# from config import OLLAMA_URL, OLLAMA_MODEL_MATH, OLLAMA_MODEL_SUMMARY

# def _call_ollama(model: str, prompt: str) -> str:
#     payload = {
#         "model": model,
#         "prompt": prompt,
#         "stream": False
#     }
#     resp = requests.post(OLLAMA_URL, json=payload)
#     resp.raise_for_status()
#     return resp.json().get("response", "").strip()

# def ask_ollama_math(prompt: str) -> str:
#     return _call_ollama(OLLAMA_MODEL_MATH, prompt)

# def ask_ollama_summary(prompt: str) -> str:
#     return _call_ollama(OLLAMA_MODEL_SUMMARY, prompt)

# # # utils/ollama_client.py

# # import requests

# # OLLAMA_URL = "http://localhost:11434/api/generate"
# # MODEL = "deepseek-r1:7b"   # best for math reasoning

# # def ask_ollama(prompt: str) -> str:
# #     payload = {
# #         "model": MODEL,
# #         "prompt": prompt,
# #         "stream": False
# #     }

# #     response = requests.post(OLLAMA_URL, json=payload)
# #     response.raise_for_status()

# #     data = response.json()
# #     return data.get("response", "")
