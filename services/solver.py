from utils.ollama_client import ask_ollama

def solve_stepwise(question: str):
    prompt = f"""
    Solve this math problem step-by-step.
    Return answer in JSON:
    {{
      "steps": ["...", "..."],
      "final_answer": "..."
    }}

    Problem: {question}
    """

    response = ask_ollama(prompt)
    return response
