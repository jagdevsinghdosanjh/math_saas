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