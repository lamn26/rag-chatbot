from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from app.services.chat_service import ChatService


@pytest.fixture
def chat_service():
    retriever = MagicMock()
    context_builder = MagicMock()
    llm = MagicMock()

    with patch.object(
        ChatService,
        "_load_prompt",
        return_value="Context:\n{context}\nQuestion: {question}",
    ):
        service = ChatService(
            retriever=retriever,
            context_builder=context_builder,
            llm=llm,
        )

    return service, retriever, context_builder, llm

def test_chat_passes_query_parameters_to_retriever(chat_service):
    service, retriever, _, _ = chat_service
    retriever.retrieve.return_value = []

    service.chat(
        question="What is RAG?",
        top_k=5,
        score_threshold=0.7,
    )

    retriever.retrieve.assert_called_once_with(
        query="What is RAG?",
        top_k=5,
        score_threshold=0.7,
    )

def test_chat_returns_fallback_when_no_results(chat_service):
    service, retriever, context_builder, llm = chat_service
    retriever.retrieve.return_value = []

    result = service.chat(
        question="What is RAG?",
        top_k=5,
    )

    assert result == {
        "answer": "I don't know based on the provided documents.",
        "sources": [],
    }
    context_builder.build.assert_not_called()
    llm.generate.assert_not_called()

def test_chat_builds_prompt_and_generates_answer(chat_service):
    service, retriever, context_builder, llm = chat_service

    results = [
        SimpleNamespace(
            payload={
                "filename": "paper.pdf",
                "page_number": 2,
                "chunk_index": 4,
                "content": "RAG combines retrieval with generation.",
            },
            score=0.92,
        )
    ]

    retriever.retrieve.return_value = results
    context_builder.build.return_value = "Retrieved context"
    llm.generate.return_value = "RAG uses retrieved information."

    result = service.chat(
        question="What is RAG?",
        top_k=3,
        score_threshold=0.6,
    )

    context_builder.build.assert_called_once_with(results=results)
    llm.generate.assert_called_once_with(
        prompt=(
            "Context:\nRetrieved context\n"
            "Question: What is RAG?"
        )
    )
    assert result["answer"] == "RAG uses retrieved information."

def test_chat_returns_source_metadata(chat_service):
    service, retriever, context_builder, llm = chat_service

    result_item = SimpleNamespace(
        payload={
            "filename": "paper.pdf",
            "page_number": 2,
            "chunk_index": 4,
            "content": "Relevant content",
        },
        score=0.92,
    )

    retriever.retrieve.return_value = [result_item]
    context_builder.build.return_value = "Relevant context"
    llm.generate.return_value = "Generated answer"

    result = service.chat(
        question="Question?",
        top_k=5,
    )

    assert result["sources"] == [
        {
            "filename": "paper.pdf",
            "page_number": 2,
            "chunk_index": 4,
            "score": 0.92,
            "content": "Relevant content",
        }
    ]

def test_chat_handles_missing_payload(chat_service):
    service, retriever, context_builder, llm = chat_service

    retriever.retrieve.return_value = [
        SimpleNamespace(payload=None, score=0.75)
    ]
    context_builder.build.return_value = "Context"
    llm.generate.return_value = "Answer"

    result = service.chat(
        question="Question?",
        top_k=5,
    )

    assert result["sources"] == [
        {
            "filename": None,
            "page_number": None,
            "chunk_index": None,
            "score": 0.75,
            "content": None,
        }
    ]