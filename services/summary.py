from utils.ollama_client import ask_ollama_summary
import json

def summarize_chapter(text: str):
    prompt = f"""
    Summarize the following chapter in simple language.
    Return STRICT JSON:
    {{
      "summary": "...",
      "key_points": ["...", "..."]
    }}

    Chapter text:
    {text}
    """

    raw = ask_ollama_summary(prompt)

    try:
        data = json.loads(raw)
        if isinstance(data, dict):
            return data
    except:
        pass

    # fallback
    return {
        "summary": raw,
        "key_points": []
    }

# from utils.ollama_client import ask_ollama

# def chapter_summary(text: str):
#     prompt = f"""
#     Summarize the following chapter in simple language.
#     Return JSON:
#     {{
#       "summary": "...",
#       "key_points": ["...", "..."]
#     }}

#     Chapter text:
#     {text}
#     """

#     response = ask_ollama(prompt)
#     return response
