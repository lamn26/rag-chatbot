from google import genai
from google.genai import types

from app.embeddings.base import BaseEmbedding

from app.core.config import settings


class CloudEmbedding(BaseEmbedding):

    def __init__(
        self,
        model_name: str = settings.CLOUD_EMBEDDING_MODEL,
        batch_size: int = 8,
        vector_size: int = settings.CLOUD_VECTOR_SIZE,
    ):
        if batch_size <= 0:
            raise ValueError("batch_size must be greater than zero.")
        if vector_size <= 0:
            raise ValueError("vector_size must be greater than zero.")

        self.model_name = model_name
        self.batch_size = batch_size
        self.vector_size = vector_size
        self.client = genai.Client(api_key=settings.API_KEY)

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        if not texts:
            return []

        all_embeddings = []

        for start in range(0, len(texts), self.batch_size):
            batch = texts[start:start + self.batch_size]
            response = self.client.models.embed_content(
                model=self.model_name,
                contents=batch,
                config=types.EmbedContentConfig(
                    output_dimensionality=self.vector_size,
                ),
            )

            if response.embeddings is None or len(response.embeddings) != len(batch):
                raise ValueError("Cloud embedding returned an unexpected number of vectors.")

            for embedding in response.embeddings:
                if embedding.values is None:
                    raise ValueError("Cloud embedding returned a vector without values.")
                all_embeddings.append(embedding.values)

        return all_embeddings

    def embed_query(
        self,
        text: str,
    ) -> list[float]:
        response = self.client.models.embed_content(
            model=self.model_name,
            contents=text,
            config=types.EmbedContentConfig(
                output_dimensionality=self.vector_size,
            ),
        )

        if not response.embeddings or response.embeddings[0].values is None:
            raise ValueError("Cloud embedding returned no query vector.")

        return response.embeddings[0].values