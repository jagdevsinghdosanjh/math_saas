import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_questions_handler(payload: dict):
    class_name = payload.get("class")
    subject = payload.get("subject")
    chapter = payload.get("chapter")
    question_type = payload.get("question_type", "mixed")
    count = payload.get("count", 10)
    difficulty = payload.get("difficulty", "mixed")

    prompt = f"""
    Generate {count} {difficulty} {question_type} questions for:
    Class: {class_name}
    Subject: {subject}
    Chapter: {chapter}

    Return JSON with fields:
    - id
    - statement
    - answer
    - solution_steps (array)
    - difficulty
    - marks
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    # return json.loads(response.choices[0].message.content)
    raw = response.choices[0].message.content or "{}"
    return json.loads(raw)


# # api/generate_questions.py

# import os
# from openai import OpenAI

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def generate_questions_handler(payload: dict):
#     """
#     Generates structured questions using GPT-4o-mini.
#     """

#     class_name = payload.get("class")
#     subject = payload.get("subject")
#     chapter = payload.get("chapter")
#     question_type = payload.get("question_type", "mixed")
#     count = payload.get("count", 10)
#     difficulty = payload.get("difficulty", "mixed")

#     prompt = f"""
#     Generate {count} {difficulty} {question_type} questions for:
#     Class: {class_name}
#     Subject: {subject}
#     Chapter: {chapter}

#     Return JSON with fields:
#     - id
#     - statement
#     - answer
#     - solution_steps (array)
#     - difficulty
#     - marks
#     """

#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[{"role": "user", "content": prompt}],
#         response_format={"type": "json_object"}
#     )

#     return response.choices[0].message.parsed
