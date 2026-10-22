import pytest
from pydantic import ValidationError

from app.schemas.chat import ChatRequest, ChatResponse, SourceItem


def test_chat_request_accepts_valid_data():
    request = ChatRequest(question="What is RAG?")

    assert request.question == "What is RAG?"
    assert request.top_k == 10
    assert request.score_threshold == 0

@pytest.mark.parametrize("question", ["", "   "])
def test_chat_request_rejects_empty_question(question):
    if question == "":
        with pytest.raises(ValidationError):
            ChatRequest(question=question)
    else:
        request = ChatRequest(question=question)
        assert request.question == question

@pytest.mark.parametrize("top_k", [0, 21])
def test_chat_request_rejects_top_k_out_of_range(top_k):
    with pytest.raises(ValidationError):
        ChatRequest(question="Question?", top_k=top_k)

@pytest.mark.parametrize("threshold", [-0.1, 1.1])
def test_chat_request_rejects_threshold_out_of_range(threshold):
    with pytest.raises(ValidationError):
        ChatRequest(
            question="Question?",
            score_threshold=threshold,
        )

def test_source_item_accepts_valid_data():
    source = SourceItem(
        filename="paper.pdf",
        page_number=2,
        chunk_index=4,
        score=0.9,
        content="Relevant content",
    )

    assert source.filename == "paper.pdf"
    assert source.score == 0.9

def test_chat_response_accepts_valid_data():
    response = ChatResponse(
        answer="This is an answer",
        sources=[
            {
                "filename": "paper.pdf",
                "page_number": 2,
                "chunk_index": 4,
                "score": 0.9,
                "content": "Relevant content",
            }
        ],
    )

    assert response.answer == "This is an answer"
    assert len(response.sources) == 1
    assert isinstance(response.sources[0], SourceItem)