from app.embeddings.base import BaseEmbedding
from app.vectorstore.base import BaseVectorStore

class Retriever:
    def __init__(
        self,
        embedding_model: BaseEmbedding,
        vector_store: BaseVectorStore,
    ):
        self.embedding_model = embedding_model
        self.vector_store = vector_store

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ):
        query_vector = self.embedding_model.embed_query(query)

        results = self.vector_store.search(
            query_vector=query_vector,
            top_k=top_k,
        )

        return results