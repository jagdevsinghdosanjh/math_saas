from utils.ollama_client import ask_ollama

def generate_questions(chapter: str, count: int = 10):
    prompt = f"""
    Generate {count} math questions for chapter: {chapter}.
    Return output strictly in JSON list format:
    [
      {{"question": "...", "answer": "..."}},
      ...
    ]
    """

    response = ask_ollama(prompt)
    return response
