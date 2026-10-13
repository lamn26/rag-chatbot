from unittest.mock import Mock, patch

from app.embeddings.cloud import CloudEmbedding
from app.embeddings.local import LocalEmbedding


def test_cloud_embedding_documents_and_query():
    documents = ["First document", "Second document", "Third document"]
    expected_vectors = [[1.0, 0.0], [0.0, 1.0], [0.5, 0.5]]

    with patch("app.embeddings.cloud.genai.Client") as client_factory:
        client = client_factory.return_value
        client.models.embed_content.side_effect = [
            Mock(embeddings=[
                Mock(values=expected_vectors[0]),
                Mock(values=expected_vectors[1]),
            ]),
            Mock(embeddings=[Mock(values=expected_vectors[2])]),
            Mock(embeddings=[Mock(values=expected_vectors[0])]),
        ]

        embedding_model = CloudEmbedding(
            model_name="test-embedding-model",
            batch_size=2,
            vector_size=2,
        )
        document_vectors = embedding_model.embed_documents(documents)
        query_vector = embedding_model.embed_query("Test query")

    assert document_vectors == expected_vectors
    assert query_vector == expected_vectors[0]
    calls = client.models.embed_content.call_args_list
    assert [call.kwargs["contents"] for call in calls] == [
        documents[:2],
        documents[2:],
        "Test query",
    ]
    assert all(
        call.kwargs["config"].output_dimensionality == 2
        for call in calls
    )


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