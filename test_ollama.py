import requests

url = "https://ollama.jsdmath.in/api/chat"

payload = {
    "model": "deepseek-r1:1.5b",
    "messages": [
        {"role": "user", "content": "Hello"}
    ]
}

resp = requests.post(url, json=payload)
print("Status:", resp.status_code)
print("Response:", resp.text)
