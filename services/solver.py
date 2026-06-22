# from utils.ollama_client import ask_ollama
from utils.ollama_client import ask_ollama_math
import json

def solve_stepwise(question: str):
    prompt = f"""
    Solve this math problem step-by-step.
    Return STRICT JSON:
    {{
      "steps": ["step 1 ...", "step 2 ..."],
      "final_answer": "..."
    }}

    Problem: {question}
    """

    raw = ask_ollama_math(prompt)

    try:
        data = json.loads(raw)
        if isinstance(data, dict):
            return data
    except:
        pass

    return {
        "steps": [raw],
        "final_answer": ""
    }


# def solve_stepwise(question: str):
#     prompt = f"""
#     Solve this math problem step-by-step.
#     Return answer in JSON:
#     {{
#       "steps": ["...", "..."],
#       "final_answer": "..."
#     }}

#     Problem: {question}
#     """

#     response = ask_ollama(prompt)
#     return response
