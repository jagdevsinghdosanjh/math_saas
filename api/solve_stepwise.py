# api/solve_stepwise.py

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def solve_stepwise_handler(payload: dict):
    """
    Evaluates a student's answer and returns step-by-step reasoning.
    """

    question_id = payload.get("question_id")
    student_answer = payload.get("student_answer", "")

    prompt = f"""
    A student answered this question:

    Question ID: {question_id}
    Student Answer: {student_answer}

    Evaluate correctness.
    Provide:
    - is_correct (true/false)
    - correct_answer
    - feedback
    - solution_steps (array)

    Return JSON only.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    return response.choices[0].message.parsed
