# services/summary.py

from utils.model_router import ask_model


def summarize_chapter(text: str) -> str:
    """
    Summarize a chapter into clear, structured notes.
    Uses the router so long prompts go to llama3 and avoid timeouts.
    """

    # Safety: trim extremely long input
    max_chars = 4000
    if len(text) > max_chars:
        text = text[:max_chars]

    prompt = (
        "You are an expert CBSE math teacher.\n"
        "Summarize the following chapter into clear, structured notes with headings and bullet points.\n\n"
        f"{text}"
    )

    return ask_model(prompt, task="summary")

# from utils.ollama_client import ask_ollama_summary
# import json

# def summarize_chapter(text: str):
#     prompt = f"""
#     Summarize the following chapter in simple language.
#     Return STRICT JSON:
#     {{
#       "summary": "...",
#       "key_points": ["...", "..."]
#     }}

#     Chapter text:
#     {text}
#     """

#     raw = ask_ollama_summary(prompt)

#     try:
#         data = json.loads(raw)
#         if isinstance(data, dict):
#             return data
#     except:
#         pass

#     # fallback
#     return {
#         "summary": raw,
#         "key_points": []
#     }