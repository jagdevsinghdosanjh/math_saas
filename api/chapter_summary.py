# api/chapter_summary.py

import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chapter_summary_handler(payload: dict):
    class_name = payload.get("class")
    subject = payload.get("subject")
    chapter = payload.get("chapter")
    language = payload.get("language", "English")
    level = payload.get("level", "basic")

    prompt = f"""
    Create a {level} summary for:
    Class: {class_name}
    Subject: {subject}
    Chapter: {chapter}
    Language: {language}

    Include:
    - summary
    - key_formulas (array)
    - common_mistakes (array)

    Return JSON only.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    # Pylance-safe fix
    raw = response.choices[0].message.content or "{}"
    return json.loads(raw)

# import os
# import json
# from openai import OpenAI

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def chapter_summary_handler(payload: dict):
#     class_name = payload.get("class")
#     subject = payload.get("subject")
#     chapter = payload.get("chapter")
#     language = payload.get("language", "English")
#     level = payload.get("level", "basic")

#     prompt = f"""
#     Create a {level} summary for:
#     Class: {class_name}
#     Subject: {subject}
#     Chapter: {chapter}
#     Language: {language}

#     Include:
#     - summary
#     - key_formulas (array)
#     - common_mistakes (array)

#     Return JSON only.
#     """

#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[{"role": "user", "content": prompt}],
#         response_format={"type": "json_object"}
#     )

#     return json.loads(response.choices[0].message.content)

# # # api/chapter_summary.py

# # import os
# # from openai import OpenAI

# # client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# # def chapter_summary_handler(payload: dict):
# #     """
# #     Generates chapter summary, formulas, and common mistakes.
# #     """

# #     class_name = payload.get("class")
# #     subject = payload.get("subject")
# #     chapter = payload.get("chapter")
# #     language = payload.get("language", "English")
# #     level = payload.get("level", "basic")

# #     prompt = f"""
# #     Create a {level} summary for:
# #     Class: {class_name}
# #     Subject: {subject}
# #     Chapter: {chapter}
# #     Language: {language}

# #     Include:
# #     - summary
# #     - key_formulas (array)
# #     - common_mistakes (array)

# #     Return JSON only.
# #     """

# #     response = client.chat.completions.create(
# #         model="gpt-4o-mini",
# #         messages=[{"role": "user", "content": prompt}],
# #         response_format={"type": "json_object"}
# #     )

# #     return response.choices[0].message.parsed
