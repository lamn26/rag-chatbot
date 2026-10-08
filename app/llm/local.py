from ollama import chat

from app.llm.base import BaseLLM

class LocalLLM(BaseLLM):
    def __init__(
        self,
        model_name: str = "qwen2.5:7b",
        temperature: float = 0,
    ):
        self.model_name = model_name
        self.temperature = temperature

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
            options={
                "temperature": self.temperature
            }
        )

        return response.message.content