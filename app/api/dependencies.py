from fastapi import (
    Depends,
    Header,
    HTTPException,
)

from app.core.session_manager import session_manager
from app.embeddings.local import LocalEmbedding
from app.vectorstore.qdrant import QdrantVectorStore
from app.retrieval.retriever import Retriever
from app.retrieval.context_builder import ContextBuilder
from app.llm.local import LocalLLM
from app.services.chat_service import ChatService

from app.ingestion.pipeline import IngestionPipeline
from app.services.document_service import DocumentService

def get_session_collection_name(
    session_id: str = Header(..., alias="X-Session-ID"),
) -> str:
    try:
        return session_manager.get_collection_name(
            session_id=session_id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        ) from e

def get_chat_service(
    collection_name: str = Depends(
        get_session_collection_name
    ),
) -> ChatService:
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

def get_document_service(
    collection_name: str = Depends(
        get_session_collection_name
    )
) -> DocumentService:
    return DocumentService(
        ingestion_pipeline=IngestionPipeline(),
        embedding_model=LocalEmbedding(),
        vector_store=QdrantVectorStore(
            collection_name=collection_name
        ),
    )