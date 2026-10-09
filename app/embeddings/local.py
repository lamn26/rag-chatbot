from ollama import embed

from app.embeddings.base import BaseEmbedding

class LocalEmbedding(BaseEmbedding):

    def __init__(
        self,
        model_name: str = "qwen3-embedding:0.6b",
        batch_size: int = 8,
    ):
        self.model_name = model_name
        self.batch_size = batch_size

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        if not texts:
            return []

        all_embeddings = []

        for start in range(0, len(texts), self.batch_size):
            batch = texts[start:start + self.batch_size]

            response = embed(
                model=self.model_name,
                input=batch,
            )

            all_embeddings.extend(response.embeddings)

        return all_embeddings

    def embed_query(
        self,
        text: str,
    ) -> list[float]:

        response = embed(
            model=self.model_name,
            input=text,
        )

        return response.embeddings[0]