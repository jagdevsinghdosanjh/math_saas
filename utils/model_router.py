# utils/model_router.py

from utils.ollama_client import ask_ollama_math, ask_ollama_summary
from utils.openai_client import ask_openai

def ask_model(prompt: str, task: str = "general") -> str:
    """
    Intelligent router:
    - Short prompts → DeepSeek (Ollama)
    - Long prompts → Llama3 (Ollama)
    - Fallback → OpenAI
    """

    try:
        if task == "math":
            return ask_ollama_math(prompt)

        if task == "summary":
            return ask_ollama_summary(prompt)

        # Default
        return ask_ollama_summary(prompt)

    except Exception:
        return ask_openai(prompt)

# # utils/model_router.py

# from utils.config import USE_OLLAMA
# from utils.ollama_client import ask_ollama_math, ask_ollama_summary

# # Optional OpenAI fallback
# try:
#     from utils.openai_client import ask_openai
# except ImportError:
#     ask_openai = None


# # Thresholds tuned for your hardware + Cloudflare timeout
# MAX_DEEPSEEK_PROMPT = 800      # deepseek-r1 safe limit on CPU
# MAX_SAFE_PROMPT = 2000         # above this → always llama3


# def ask_model(prompt: str, task: str = "general") -> str:
#     """
#     Unified intelligent model router.
#     task = "math", "summary", "questions", "chat", "general"
#     """

#     length = len(prompt)

#     # 1. Very long prompts → always llama3 (avoid 524)
#     if length > MAX_SAFE_PROMPT:
#         return _use_summary_model(prompt)

#     # 2. Math tasks
#     if task == "math":
#         # Short math → deepseek-r1 (better reasoning)
#         if length < MAX_DEEPSEEK_PROMPT:
#             return _use_math_model(prompt)
#         # Long math → llama3 (safer)
#         return _use_summary_model(prompt)

#     # 3. Question generation (heavy text)
#     if task == "questions":
#         return _use_summary_model(prompt)

#     # 4. Summaries
#     if task == "summary":
#         return _use_summary_model(prompt)

#     # 5. Chat / general
#     if task == "chat":
#         return _use_summary_model(prompt)

#     # 6. Fallback
#     return _use_summary_model(prompt)


# # -----------------------------
# # Internal helpers
# # -----------------------------

# def _use_math_model(prompt: str) -> str:
#     if USE_OLLAMA:
#         return ask_ollama_math(prompt)
#     if ask_openai:
#         return ask_openai(prompt)
#     return "No model available."


# def _use_summary_model(prompt: str) -> str:
#     if USE_OLLAMA:
#         return ask_ollama_summary(prompt)
#     if ask_openai:
#         return ask_openai(prompt)
#     return "No model available."

# # # utils/model_router.py

# # from utils.config import USE_OLLAMA
# # from utils.ollama_client import ask_ollama_math, ask_ollama_summary

# # # Optional fallback (only if you still use OpenAI)
# # try:
# #     from utils.openai_client import ask_openai
# # except ImportError:
# #     ask_openai = None


# # def ask_model_math(prompt: str) -> str:
# #     if USE_OLLAMA:
# #         return ask_ollama_math(prompt)
# #     if ask_openai:
# #         return ask_openai(prompt)
# #     return "No model available."


# # def ask_model_summary(prompt: str) -> str:
# #     if USE_OLLAMA:
# #         return ask_ollama_summary(prompt)
# #     if ask_openai:
# #         return ask_openai(prompt)
# #     return "No model available."

# # # from config import USE_OLLAMA
# # # from utils.ollama_client import ask_ollama_math, ask_ollama_summary

# # # # Optional fallback (only if you still use OpenAI)
# # # try:
# # #     from utils.openai_client import ask_openai
# # # except ImportError:
# # #     ask_openai = None


# # # def ask_model_math(prompt: str) -> str:
# # #     if USE_OLLAMA:
# # #         return ask_ollama_math(prompt)
# # #     if ask_openai:
# # #         return ask_openai(prompt)
# # #     return "No model available."


# # # def ask_model_summary(prompt: str) -> str:
# # #     if USE_OLLAMA:
# # #         return ask_ollama_summary(prompt)
# # #     if ask_openai:
# # #         return ask_openai(prompt)
# # #     return "No model available."
