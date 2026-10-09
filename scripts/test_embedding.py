from app.embeddings.local import LocalEmbedding

def main():
    embedding_model = LocalEmbedding()

    documents = [
        "The Transformer uses attention mechanisms.",
        "Paris is the capital of France.",
        "Con mèo đang nằm trên ghế sofa.",
    ]

    document_vectors = embedding_model.embed_documents(
        documents
    )

    query_vector = embedding_model.embed_query(
        "What is the Transformer architecture?"
    )

    print("Number of document embeddings:", len(document_vectors))
    print("Document embedding dimension:", len(document_vectors[0]))
    print("Query embedding dimension:", len(query_vector))

    assert len(document_vectors) == len(documents)
    assert len(document_vectors[0]) == len(query_vector)
    assert all(len(vector) == len(query_vector) for vector in document_vectors)

    print("Embedding test passed!")


if __name__ == "__main__":
    main()