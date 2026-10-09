from functools import lru_cache

from app.embeddings.local import LocalEmbedding
from app.vectorstore.qdrant import QdrantVectorStore
from app.retrieval.retriever import Retriever
from app.retrieval.context_builder import ContextBuilder
from app.llm.local import LocalLLM
from app.services.chat_service import ChatService


@lru_cache(maxsize=1)
def get_chat_service() -> ChatService:
    embedding_model = LocalEmbedding()

    vector_store = QdrantVectorStore(
        collection_name="documents"
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