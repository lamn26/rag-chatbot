from ollama import Client

from app.embeddings.base import BaseEmbedding
from app.core.config import settings

class LocalEmbedding(BaseEmbedding):

    def __init__(
        self,
        model_name: str | None = None,
        batch_size: int = 8,
    ):
        self.model_name = model_name or settings.LOCAL_EMBEDDING_MODEL
        self.batch_size = batch_size
        self.client = Client(host=settings.OLLAMA_BASE_URL)

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        if not texts:
            return []

        all_embeddings = []

        for start in range(0, len(texts), self.batch_size):
            batch = texts[start:start + self.batch_size]

            response = self.client.embed(
                model=self.model_name,
                input=batch,
            )

            all_embeddings.extend(response.embeddings)

        return all_embeddings

    def embed_query(
        self,
        text: str,
    ) -> list[float]:

        response = self.client.embed(
            model=self.model_name,
            input=text,
        )

        return response.embeddings[0]