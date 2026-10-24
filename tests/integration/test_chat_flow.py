from fastapi.testclient import TestClient

from app.main import app
from app.api.dependencies import get_chat_service

class FakeRetriever:
    def retrieve(
        self,
        query: str,
        top_k: int,
        score_threshold: float = 0,
    ):
        return [
            type(
                "FakeResult",
                (),
                {
                    "payload": {
                        "filename": "attention.pdf",
                        "page_number": 1,
                        "chunk_index": 0,
                        "content": "The Transformer uses attention mechanisms.",
                    },
                    "score": 0.92,
                },
            )()
        ]

class FakeContextBuilder:
    def build(self, results):
        return "\n".join(
            result.payload["content"] for result in results
        )

class FakeLLM:
    def generate(self, prompt: str) -> str:
        assert "The Transformer uses attention mechanisms." in prompt
        assert "What does the Transformer use?" in prompt
        return "The Transformer uses attention mechanisms."

def test_chat_api_returns_answer_and_sources():
    from app.services.chat_service import ChatService

    def override_chat_service():
        return ChatService(
            retriever=FakeRetriever(),
            context_builder=FakeContextBuilder(),
            llm=FakeLLM()
        )

    app.dependency_overrides[get_chat_service] = override_chat_service

    try:
        client = TestClient(app=app)

        response = client.post(
            "api/v1/chat",
            json={
                "question": "What does the Transformer use?",
                "top_k": 5,
                "score_threshold": 0,
            },
        )

        assert response.status_code == 200

        body = response.json()

        assert body["answer"] == "The Transformer uses attention mechanisms."

        assert len(body["sources"]) == 1

        source = body["sources"][0]
        assert source["filename"] == "attention.pdf"
        assert source["page_number"] == 1
        assert source["chunk_index"] == 0
        assert source["score"] == 0.92
        assert source["content"] == "The Transformer uses attention mechanisms."

    finally:
        app.dependency_overrides.pop(
            get_chat_service,
            None
        )