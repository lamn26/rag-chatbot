from app.vectorstore.base import BaseVectorStore
from app.core.config import settings

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
    FilterSelector,
)

class QdrantVectorStore(BaseVectorStore):
    def __init__(
        self,
        collection_name: str,
        url: str | None = None,
    ):
        self.client = QdrantClient(
            url=url or settings.QDRANT_URL,
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
        embeddings,
        batch_size: int = 8,
    ) -> None:
        if len(documents) != len(embeddings):
            raise ValueError(
                "The number of documents must match "
                "the number of embeddings."
            )

        if batch_size < 1:
            raise ValueError("batch_size must be at least 1.")

        total_documents = len(documents)

        for start in range(0, total_documents, batch_size):
            end = min(start + batch_size, total_documents)

            batch_documents = documents[start:end]
            batch_embeddings = embeddings[start:end]

            points = []

            for document, embedding in zip(
                batch_documents,
                batch_embeddings,
            ):
                payload = {
                    "content": document.content,
                    **document.metadata,
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
                wait=True,
            )

        print(
            f"Uploaded successful !"
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

    def list_documents(self) -> list[dict]:
        documents = {}

        offset = None

        while True:
            points, next_offset = self.client.scroll(
                collection_name=self.collection_name,
                limit=256,
                offset=offset,
                with_payload=True,
                with_vectors=True,
            )

            for point in points:
                payload = point.payload or {}

                document_id = payload.get("document_id")
                filename = payload.get("filename")

                if not document_id:
                    continue

                if document_id not in documents:
                    documents[document_id] = {
                        "document_id": document_id,
                        "filename": filename or "unknown",
                        "chunks_count": 0,
                    }

                documents[document_id]["chunks_count"] += 1

            if next_offset is None:
                break

            offset = next_offset

        return list(documents.values())

    def get_document_by_id(self, document_id: str) -> dict | None:
        points, _ = self.client.scroll(
            collection_name=self.collection_name,
            scroll_filter={
                "must": [
                    {
                        "key": "document_id",
                        "match": {"value": document_id}
                    }
                ]
            },
            limit=1,
            with_payload=True,
            with_vectors=False,
        )

        if not points:
            return None

        payload = points[0].payload or {}

        return {
            "document_id": document_id,
            "filename": payload.get("filename", "unknown"),
            "metadata": {
                "file_directory": payload.get("file_directory"),
                "last_modified": payload.get("last_modified"),
                "filetype": payload.get("filetype"),
                "source": payload.get("source"),
                "languages": payload.get("languages"),
            }
        }

    def delete_document(self, document_id: str) -> None:
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=FilterSelector(
                filter=Filter(
                    must=[
                        FieldCondition(
                            key="document_id",
                            match=MatchValue(value=document_id)
                        )
                    ]
                )
            ),
            wait=True,
        )

    def check_document_exist_by_hash(self, file_hash: str) -> bool:
        points, _ = self.client.scroll(
            collection_name=self.collection_name,
            scroll_filter={
                "must": [
                    {
                        "key": "file_hash",
                        "match": {"value": file_hash}
                    }
                ]
            },
            limit=1,
            with_payload=True,
            with_vectors=False,
        )

        return len(points) > 0

    def delete_collection(self) -> None:
        self.client.delete_collection(
            collection_name=self.collection_name
        )

    