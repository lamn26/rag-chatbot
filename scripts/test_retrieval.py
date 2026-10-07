from app.embeddings.local import LocalEmbedding
from app.vectorstore.qdrant import QdrantVectorStore
from app.retrieval.retriever import Retriever
from app.retrieval.context_builder import ContextBuilder

def main():
    embedding_model = LocalEmbedding()

    vector_store = QdrantVectorStore(
        collection_name="documents"
    )

    retriever = Retriever(
        embedding_model=embedding_model,
        vector_store=vector_store,
    )

    context_builder = ContextBuilder()

    # Query
    query = "How does multi-head attention work?"
    print(f"\nQuery: {query}\n")

    # Retrieve
    results = retriever.retrieve(
        query=query,
        top_k=5,
    )
    print(f"Retrieved {len(results)} results\n")

    for index, result in enumerate(results):
        payload = result.payload or {}

        print("-"*80)

        print(f"Results #{index+1}")

        print(f"Score: {result.score:4f}")

        print(f"Source: {payload.get('filename')}")

        print(f"Page: {payload.get('page_number')}")

        print(f"Chunk: {payload.get('chunk_index')}")

        print(f"\nContent:\n{payload.get('content', '')}")

    # Context
    context = context_builder.build(
        results=results
    )

    print("\n\n")
    print("-" * 80)
    print("FINAL CONTEXT")
    print("-" * 80)

    print(context)

if __name__ =="__main__":
    main()