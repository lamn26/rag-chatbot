from functools import lru_cache

from app.embeddings.local import LocalEmbedding
from app.vectorstore.qdrant import QdrantVectorStore
from app.retrieval.retriever import Retriever
from app.retrieval.context_builder import ContextBuilder
from app.llm.local import LocalLLM
from app.services.chat_service import ChatService

from app.ingestion.pipeline import IngestionPipeline
from app.services.document_service import DocumentService

collection_name = "documents_qwen3"

@lru_cache(maxsize=1)
def get_chat_service() -> ChatService:
    embedding_model = LocalEmbedding()

    vector_store = QdrantVectorStore(
        collection_name=collection_name
    )

    retriever = Retriever(
        embedding_model=embedding_model,
        vector_store=vector_store,
    )

    context_builder = ContextBuilder()

    llm = LocalLLM()

    return ChatService(
        retriever=retriever,
        context_builder=context_builder,
        llm=llm,
    )

@lru_cache(maxsize=1)
def get_document_service() -> DocumentService:
    return DocumentService(
        ingestion_pipeline=IngestionPipeline(),
        embedding_model=LocalEmbedding(),
        vector_store=QdrantVectorStore(
            collection_name="documents_qwen3"
        ),
    )