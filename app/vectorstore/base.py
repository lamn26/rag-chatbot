from abc import ABC, abstractmethod


class BaseVectorStore(ABC):

    @abstractmethod
    def create_collection(
        self,
        vector_size: int,
    ) -> None:
        pass

    @abstractmethod
    def add_documents(
        self,
        documents,
        embeddings,
    ) -> None:
        pass

    @abstractmethod
    def search(
        self,
        query_vector,
        top_k: int = 5,
        score_threshold: float | None = None,
    ):
        pass