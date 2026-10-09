from app.ingestion.pipeline import IngestionPipeline
from app.embeddings.local import LocalEmbedding
from app.vectorstore.qdrant import QdrantVectorStore

folder_path = "data/raw"
collection_name = "documents_qwen3"
batch_size = 8

def main():
    #1. Ingestion
    print("Ingesting ....")

    pipeline = IngestionPipeline()
    chunks = pipeline.process_folder(
        folder_path=folder_path
    )

    print(f"Created {len(chunks)} chunks.")

    #2. Embedding
    print("\nLoading model ....")
    embedding_model = LocalEmbedding(
        batch_size=batch_size
    )

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
        collection_name=collection_name
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