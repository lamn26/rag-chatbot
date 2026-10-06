from app.embeddings.local import LocalEmbedding
import numpy as np

def main():

    embedding_model = LocalEmbedding()

    documents = [
        "The Transformer architecture is based entirely on attention mechanisms.",
        "Transformers do not use recurrent neural networks.",
        "Convolutional neural networks are commonly used for image processing.",
    ]

    print("Generating document embeddings...")

    embeddings = embedding_model.embed_documents(
        documents
    )

    print(
        f"Number of embeddings: {len(embeddings)}"
    )

    print(
        f"Embedding dimension: {len(embeddings[0])}"
    )

    print(
        f"First 10 values:\n{embeddings[0][:10]}"
    )

    query = "What is the Transformer architecture?"

    print("\nGenerating query embedding...")

    query_embedding = embedding_model.embed_query(
        query
    )

    print(
        f"Query embedding dimension: "
        f"{len(query_embedding)}"
    )

    print(
        f"First 10 values:\n"
        f"{query_embedding[:10]}"
    )

    print("\nSimilarity with each document:")

    query_vector = np.array(query_embedding)

    for index, embedding in enumerate(embeddings):

        document_vector = np.array(embedding)

        similarity = np.dot(
            query_vector,
            document_vector,
        )

        print(
            f"Document {index + 1}: "
            f"{similarity:.4f}"
        )


if __name__ == "__main__":
    main()