from sentence_transformers import SentenceTransformer

from app.embeddings.base import BaseEmbedding


class LocalEmbedding(BaseEmbedding):

    def __init__(
        self,
        model_name: str = "intfloat/multilingual-e5-small",
    ):
        self.model = SentenceTransformer(model_name)

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        texts = [
            f"passage: {text}"
            for text in texts
        ]

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
        )

        return embeddings.tolist()

    def embed_query(
        self,
        text: str,
    ) -> list[float]:

        embedding = self.model.encode(
            f"query: {text}",
            normalize_embeddings=True,
        )

        return embedding.tolist()