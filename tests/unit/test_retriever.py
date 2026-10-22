from unittest.mock import MagicMock

from app.retrieval.retriever import Retriever

def test_retrieve_embeds_query():
    embedding_model = MagicMock()
    vector_store = MagicMock()

    embedding_model.embed_query.return_value = [0.1, 0.2, 0.3]
    vector_store.search.return_value = []

    retriever = Retriever(embedding_model, vector_store)
    retriever.retrieve("What is RAG?", top_k=3)

    embedding_model.embed_query.assert_called_once_with(
        "What is RAG?"
    )

def test_retrieve_passes_arguments_to_vector_store():
    embedding_model = MagicMock()
    vector_store = MagicMock()

    embedding_model.embed_query.return_value = [0.1, 0.2, 0.3]
    vector_store.search.return_value = []

    retriever = Retriever(embedding_model, vector_store)
    retriever.retrieve(
        "What is RAG?",
        top_k=5,
        score_threshold=0.7,
    )

    vector_store.search.assert_called_once_with(
        query_vector=[0.1, 0.2, 0.3],
        top_k=5,
        score_threshold=0.7,
    )

def test_retrieve_passes_none_threshold():
    embedding_model = MagicMock()
    vector_store = MagicMock()

    embedding_model.embed_query.return_value = [0.1, 0.2, 0.3]
    vector_store.search.return_value = []

    retriever = Retriever(embedding_model, vector_store)
    retriever.retrieve("Hello", top_k=2)

    vector_store.search.assert_called_once_with(
        query_vector=[0.1, 0.2, 0.3],
        top_k=2,
        score_threshold=None,
    )

def test_retrieve_returns_vector_store_results():
    embedding_model = MagicMock()
    vector_store = MagicMock()

    expected_results = [
        {"content": "Relevant chunk 1", "score": 0.9},
        {"content": "Relevant chunk 2", "score": 0.8},
    ]

    embedding_model.embed_query.return_value = [0.1, 0.2, 0.3]
    vector_store.search.return_value = expected_results

    retriever = Retriever(embedding_model, vector_store)
    result = retriever.retrieve("What is RAG?", top_k=2)

    assert result is expected_results