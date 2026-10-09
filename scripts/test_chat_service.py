from app.embeddings.local import LocalEmbedding
from app.vectorstore.qdrant import QdrantVectorStore

from app.retrieval.retriever import Retriever
from app.retrieval.context_builder import ContextBuilder

from app.llm.local import LocalLLM

from app.services.chat_service import ChatService

collection_name = "documents_qwen3"

def main():
    embedding_model = LocalEmbedding()

    vector_store = QdrantVectorStore(
        collection_name=collection_name
    )

    retriever = Retriever(
        embedding_model=embedding_model,
        vector_store=vector_store
    )

    context_builder = ContextBuilder()

    llm = LocalLLM()

    chat_service = ChatService(
        retriever=retriever,
        context_builder=context_builder,
        llm=llm
    )

    # question = "What is the Transformer architecture?"
    question = "What is the capital of France?"

    result = chat_service.chat(
        question=question,
        top_k=5,
        score_threshold=None
    )

    print("\n" + "-" * 80)
    print("QUESTION")
    print("-" * 80)

    print(question)

    print("\n" + "-" * 80)
    print("ANSWER")
    print("-" * 80)

    print(result["answer"])

    print("\n" + "-" * 80)
    print("SOURCES")
    print("-" * 80)

    for source in result["sources"]:
        print(source)


if __name__ == "__main__":
    main()