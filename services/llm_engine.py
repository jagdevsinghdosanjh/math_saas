import openai

class CodexEngine:
    def __init__(self, api_key: str):
        openai.api_key = api_key

    async def generate(self, prompt: str):
        response = openai.Completion.create(
            model="code-davinci-002",
            prompt=prompt,
            max_tokens=500,
            temperature=0.2,
            stop=None
        )
        return response["choices"][0]["text"].strip()
def get_engine(engine_name: str):
    if engine_name == "ollama":
        return OllamaEngine()
    if engine_name == "openai":
        return OpenAIEngine()
    if engine_name == "codex":
        return CodexEngine(api_key=OPENAI_API_KEY)
