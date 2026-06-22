import json
from utils.model_router import ask_model_math

def generate_questions(chapter: str, count: int = 10) -> list:
    prompt = f"""
    You are a math question generator.

    Chapter/topic: {chapter}
    Generate {count} questions of mixed difficulty.
    Return STRICTLY valid JSON (no extra text), in this format:

    [
      {{"question": "...", "answer": "...", "difficulty": "easy|medium|hard"}},
      ...
    ]
    """

    raw = ask_model_math(prompt)

    try:
        data = json.loads(raw)
        if isinstance(data, list):
            return data
    except Exception:
        pass

    return [{"question": raw, "answer": "", "difficulty": "unknown"}]

# from utils.ollama_client import ask_ollama
# from utils.config import USE_OLLAMA
# from utils.ollama_client import ask_ollama
# from utils.model_router import ask_model_math # your existing file

# def generate_questions(chapter: str, count: int = 10):
#     prompt = f"""
#     Generate {count} math questions for chapter: {chapter}.
#     Return output strictly in JSON list format:
#     [
#       {{"question": "...", "answer": "..."}},
#       ...
#     ]
#     """

#     response = ask_ollama(prompt)
#     return response
