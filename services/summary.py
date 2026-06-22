from utils.ollama_client import ask_ollama

def chapter_summary(text: str):
    prompt = f"""
    Summarize the following chapter in simple language.
    Return JSON:
    {{
      "summary": "...",
      "key_points": ["...", "..."]
    }}

    Chapter text:
    {text}
    """

    response = ask_ollama(prompt)
    return response
