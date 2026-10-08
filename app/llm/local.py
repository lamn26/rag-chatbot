from ollama import chat

from app.llm.base import BaseLLM

class LocalLLM(BaseLLM):
    def __init__(
        self,
        model_name: str = "qwen2.5:1.5b",
    ):
        self.model_name = model_name

    def generate(
        self,
        prompt,
    ):
        response = chat(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        return response.message.content