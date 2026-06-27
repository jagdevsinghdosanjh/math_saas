# utils/health.py

import time
import requests
from requests.exceptions import RequestException, Timeout
from utils.config import (
    OLLAMA_URL,
    OLLAMA_MODEL_MATH,
    OLLAMA_MODEL_MATH_HEAVY,
    OLLAMA_MODEL_SUMMARY,
)

TIMEOUT = 8


def check_endpoint(url: str, payload: dict):
    """
    Returns (ok: bool, latency_ms: int | None)
    """
    start = time.time()
    try:
        r = requests.post(url, json=payload, timeout=TIMEOUT)
        latency = round((time.time() - start) * 1000)
        return r.status_code == 200, latency
    except (RequestException, Timeout):
        return False, None


def health_check():
    """
    Returns a dict with health status for:
    - Local API
    - Tunnel API
    - DeepSeek 1.5B
    - DeepSeek 7B
    - Llama 3.2
    """
    results: dict[str, bool | int | None] = {}

    # 1. Local API
    try:
        r = requests.get("https://ollama.jsdmath.in/api/tags", timeout=TIMEOUT)
        # r = requests.get("http://localhost:11434/api/tags", timeout=TIMEOUT)
        results["local_api"] = r.status_code == 200
    except (RequestException, Timeout):
        results["local_api"] = False

    # 2. Tunnel API
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=TIMEOUT)
        results["tunnel_api"] = r.status_code == 200
    except (RequestException, Timeout):
        results["tunnel_api"] = False

    # 3. DeepSeek 1.5B
    ok, latency = check_endpoint(
        f"{OLLAMA_URL}/api/generate",
        {"model": OLLAMA_MODEL_MATH, "prompt": "hi", "stream": False},
    )
    results["deepseek_1_5b"] = ok
    results["deepseek_1_5b_latency"] = latency

    # 4. DeepSeek 7B
    ok, latency = check_endpoint(
        f"{OLLAMA_URL}/api/generate",
        {"model": OLLAMA_MODEL_MATH_HEAVY, "prompt": "hi", "stream": False},
    )
    results["deepseek_7b"] = ok
    results["deepseek_7b_latency"] = latency

    # 5. Llama 3.2
    ok, latency = check_endpoint(
        f"{OLLAMA_URL}/api/generate",
        {"model": OLLAMA_MODEL_SUMMARY, "prompt": "hi", "stream": False},
    )
    results["llama_3_2"] = ok
    results["llama_3_2_latency"] = latency

    return results
