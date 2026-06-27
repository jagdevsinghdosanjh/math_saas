# utils/health.py
import streamlit as st
import requests
import psutil
import pandas as pd
import time
from requests.exceptions import RequestException, Timeout
from utils.config import (
    OLLAMA_URL,
    OLLAMA_MODEL_MATH,
    OLLAMA_MODEL_MATH_HEAVY,
    OLLAMA_MODEL_SUMMARY,
)

TIMEOUT = 25 #insted of 8 for heavy_math_model to respond correctly

def host_ram_monitor(base_url: str = "http://localhost:5055"):
    """
    Fetches host RAM from Windows RAM API bridge.
    Returns dict with total_gb, used_gb, free_gb or error.
    """
    try:
        resp = requests.get(f"{base_url}/ram", timeout=3)
        resp.raise_for_status()
        data = resp.json()

        return {
            "total_gb": data.get("total_gb"),
            "used_gb": data.get("used_gb"),
            "free_gb": data.get("free_gb"),
        }
    except Exception as e:
        return {
            "error": str(e),
            "total_gb": None,
            "used_gb": None,
            "free_gb": None,
        }


def run_health_monitor():
    st.title("System Health Monitor - Of Container")
    st.caption("Local RAM, CPU, and Ollama Model Status")

    # --- SYSTEM METRICS ---
    ram = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=1)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total RAM", f"{ram.total / (1024**3):.2f} GB")
        st.metric("Used RAM", f"{ram.used / (1024**3):.2f} GB")
        st.metric("Free RAM", f"{ram.available / (1024**3):.2f} GB")

    with col2:
        st.metric("CPU Usage", f"{cpu}%")
        st.metric("Processes Running", len(psutil.pids()))

    st.divider()

    # --- MODEL STATUS ---
    st.subheader("📦 Loaded Models")

    try:
        data = requests.get("https://ollama.jsdmath.in/api/ps", timeout=2).json()
        models = data.get("models", [])
    except Exception as e:
        print(f"Health check error: {e}")

        models = []

    if not models:
        st.error("No models loaded in RAM")
    else:
        df = pd.DataFrame([
            {
                "Model": m["name"],
                "Size (GB)": m["size"] / (1024**3),
                "Context Length": m["details"].get("context_length", 4096),
                "Expires At": m.get("expires_at", "N/A")
            }
            for m in models
        ])
        st.dataframe(df, use_container_width=True)

    st.divider()

    # --- PROCESS TABLE ---
    st.subheader("⚙️ Ollama Processes")

    processes = []
    for p in psutil.process_iter(['pid', 'name', 'memory_info', 'cpu_percent']):
        if "ollama" in p.info['name'].lower():
            processes.append({
                "PID": p.info['pid'],
                "CPU %": p.info['cpu_percent'],
                "RAM (MB)": p.info['memory_info'].rss / (1024**2)
            })

    if processes:
        st.dataframe(pd.DataFrame(processes), use_container_width=True)
    else:
        st.warning("No Ollama processes detected")

    st.info("Auto-refresh every 5 seconds")


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
        {"model": OLLAMA_MODEL_MATH, "prompt": "Hi", "stream": False},
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
