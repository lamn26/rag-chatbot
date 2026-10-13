from google import genai
from google.genai import types

from app.llm.base import BaseLLM
from app.core.config import settings


class CloudLLM(BaseLLM):
    def __init__(
        self,
        model_name: str = settings.CLOUD_LLM_MODEL,
        temperature: float = 0,
    ):
        self.model_name = model_name
        self.temperature = temperature
        self.client = genai.Client(api_key=settings.API_KEY)

    def generate(
        self,
        prompt: str,
    ) -> str:
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=self.temperature,
            ),
        )

        if response.text is None:
            raise ValueError("Cloud LLM returned an empty response.")

        return response.text