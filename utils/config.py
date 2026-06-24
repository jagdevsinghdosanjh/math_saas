# config.py

"""
Global configuration for math_saas.
Controls:
- Ollama usage
- Model selection
- API endpoints
"""

# Enable or disable Ollama engine
USE_OLLAMA = True

# Public Ollama endpoint (via Cloudflare Tunnel)
OLLAMA_URL = "https://ollama.jsdmath.in/api/generate"

# Model assignments
# Math/logic model (used only for short prompts via router)
OLLAMA_MODEL_MATH = "deepseek-r1:7b"

# Fast text model (default for summaries, questions, long prompts)
# IMPORTANT: Only use models that exist on your server
OLLAMA_MODEL_SUMMARY = "deepseek-r1:7b"
