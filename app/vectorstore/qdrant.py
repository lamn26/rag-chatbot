from app.vectorstore.base import BaseVectorStore

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
)

class QdrantVectorStore(BaseVectorStore):
    def __init__(
        self,
        collection_name: str,
        url: str="http://localhost:6333",
    ):
        self.client = QdrantClient(
            url=url,
        )

        self.collection_name = collection_name

    def create_collection(
        self,
        vector_size: int
    ) -> None:
        collections = self.client.get_collections()

        existing_name = [
            collection.name
            for collection in collections.collections
        ]

        if self.collection_name in existing_name:
            return

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE,
            ),
        )

    def add_documents(
        self,
        documents,
        embeddings
    ) -> None:
        points = []

        for document, embedding in zip(documents, embeddings):
            payload = {
                "content": document.content,
                **document.metadata
            }

            point = PointStruct(
                id=document.chunk_id,
                vector=embedding,
                payload=payload,
            )

            points.append(point)

        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
        )

    def search(
        self,
        query_vector,
        top_k: int = 5,
        score_threshold: float | None = None,
    ):

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=top_k,
            score_threshold=score_threshold
        )

        return results.points