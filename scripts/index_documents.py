from app.ingestion.pipeline import IngestionPipeline
from app.embeddings.local import LocalEmbedding
from app.vectorstore.qdrant import QdrantVectorStore


def main():

    file_path = (
        "data/raw/Attention Is All You Need.pdf"
    )

    #1. Ingestion
    print("Ingesting ....")

    pipeline = IngestionPipeline()
    chunks = pipeline.process(
        file_path=file_path
    )

    print(f"Created {len(chunks)} chunks.")

    #2. Embedding
    print("\nLoading model ....")
    embedding_model = LocalEmbedding()

    print("\nGenerating ....")
    texts = [chunk.content for chunk in chunks]

    embeddings = embedding_model.embed_documents(texts=texts)

    print(
        f"Generated {len(embeddings)} embeddings."
    )

    print(
        f"Embedding dimension: "
        f"{len(embeddings[0])}"
    )

    #3. Qdrant
    print("\nConnecting ....")

    vector_store = QdrantVectorStore(
        collection_name="documents"
    )

    vector_store.create_collection(
        vector_size=len(embeddings[0])
    )

    #4. Store
    print("Uploading ....")

    vector_store.add_documents(
        documents=chunks,
        embeddings=embeddings,
    )

    print("\nIndexing completed.")


if __name__ == "__main__":
    main()