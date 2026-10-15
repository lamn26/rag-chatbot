from ollama import Client

from app.llm.base import BaseLLM
from app.core.config import settings

class LocalLLM(BaseLLM):
    def __init__(
        self,
        model_name: str |None = None,
        temperature: float = 0,
    ):
        self.model_name = model_name or settings.LOCAL_LLM_MODEL
        self.temperature = temperature
        self.client = Client(host=settings.OLLAMA_BASE_URL)

    def generate(
        self,
        prompt,
    ):
        response = self.client.chat(
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