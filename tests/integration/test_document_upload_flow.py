from fastapi.testclient import TestClient

from app.main import app
from app.api.dependencies import get_document_service
from app.services.document_service import DocumentService
from app.ingestion.pipeline import IngestionPipeline


class FakeEmbedding:
    def embed_documents(self, texts: list[str]):
        return [[0.1, 0.2, 0.3] for _ in texts]


class FakeVectorStore:
    def __init__(self):
        self.documents = []
        self.embeddings = []

    def check_document_exist_by_hash(self, file_hash: str) -> bool:
        return any(
            chunk.metadata.get("file_hash") == file_hash
            for chunk in self.documents
        )

    def add_documents(self, documents, embeddings):
        self.documents.extend(documents)
        self.embeddings.extend(embeddings)

    def list_documents(self):
        grouped = {}

        for chunk in self.documents:
            document_id = chunk.document_id

            if document_id not in grouped:
                grouped[document_id] = {
                    "document_id": document_id,
                    "filename": chunk.metadata["filename"],
                    "chunks_count": 0,
                }

            grouped[document_id]["chunks_count"] += 1

        return list(grouped.values())

    def get_document_by_id(self, document_id: str):
        for chunk in self.documents:
            if chunk.document_id == document_id:
                return {
                    "document_id": document_id,
                    "filename": chunk.metadata["filename"],
                    "metadata": chunk.metadata,
                }

        return None

    def delete_document(self, document_id: str):
        remaining_documents = []
        remaining_embeddings = []

        for chunk, embedding in zip(
            self.documents,
            self.embeddings,
        ):
            if chunk.document_id != document_id:
                remaining_documents.append(chunk)
                remaining_embeddings.append(embedding)

        self.documents = remaining_documents
        self.embeddings = remaining_embeddings

def test_upload_txt_document_through_api(
    tmp_path,
    monkeypatch,
):
    vector_store = FakeVectorStore()

    def override_document_service():
        return DocumentService(
            ingestion_pipeline=IngestionPipeline(),
            embedding_model=FakeEmbedding(),
            vector_store=vector_store,
            session_id="integration-test-session",
        )

    app.dependency_overrides[get_document_service] = (
        override_document_service
    )

    monkeypatch.chdir(tmp_path)

    try:
        client = TestClient(app=app)

        response = client.post(
            "/api/v1/documents/upload",
            files={
                "file": (
                    "sample.txt",
                    b"Retrieval augmented generation combines retrieval and generation.",
                    "text/plain",
                )
            },
        )

        assert response.status_code == 201

        body = response.json()
        assert body["filename"] == "sample.txt"
        assert body["status"] == "completed"
        assert body["chunks_created"] > 0
        assert body["document_id"]

        assert len(vector_store.documents) == body["chunks_created"]
        assert len(vector_store.embeddings) == body["chunks_created"]

        for chunk in vector_store.documents:
            assert chunk.content
            assert chunk.metadata["filename"] == "sample.txt"
            assert chunk.metadata["source"] == "sample.txt"
            assert chunk.metadata["file_hash"]
        
    finally:
        app.dependency_overrides.pop(
            get_document_service,
            None,
        )

def test_upload_unsupported_file_returns_400(
    tmp_path,
    monkeypatch,
):
    vector_store = FakeVectorStore()

    def override_document_service():
        return DocumentService(
            ingestion_pipeline=IngestionPipeline(),
            embedding_model=FakeEmbedding(),
            vector_store=vector_store,
            session_id="integration-test-session",
        )

    app.dependency_overrides[get_document_service] = (
        override_document_service
    )

    monkeypatch.chdir(tmp_path)

    try:
        client = TestClient(app=app)

        response = client.post(
            "/api/v1/documents/upload",
            files={
                "file": (
                    "sample.exe",
                    b"unsupported file content",
                    "application/octet-stream",
                )
            },
        )

        assert response.status_code == 400
        assert response.json()["detail"] == (
            "Unsupported file type: .exe"
        )

        assert vector_store.documents == []
        assert vector_store.embeddings == []

    finally:
        app.dependency_overrides.pop(
            get_document_service,
            None,
        )

def test_upload_duplicate_document_returns_409(
    tmp_path,
    monkeypatch,
):
    vector_store = FakeVectorStore()

    def override_document_service():
        return DocumentService(
            ingestion_pipeline=IngestionPipeline(),
            embedding_model=FakeEmbedding(),
            vector_store=vector_store,
            session_id="integration-test-session",
        )

    app.dependency_overrides[get_document_service] = (
        override_document_service
    )

    monkeypatch.chdir(tmp_path)

    content = (
        b"Retrieval augmented generation combines retrieval "
        b"and generation."
    )

    try:
        client = TestClient(app=app)

        first_response = client.post(
            "api/v1/documents/upload",
            files={
                "file": ("sample.txt", content, "text/plain")
            },
        )

        assert first_response.status_code == 201

        second_response = client.post(
            "/api/v1/documents/upload",
            files={
                "file": ("sample-copy.txt", content, "text/plain")
            },
        )

        assert second_response.status_code == 409

        assert len(vector_store.documents) > 0
        assert len(vector_store.embeddings) == len(vector_store.documents)

        assert len(vector_store.documents) == first_response.json()["chunks_created"]

    finally:
        app.dependency_overrides.pop(
            get_document_service,
            None,
        )

def test_list_documents_through_api(tmp_path, monkeypatch):
    vector_store = FakeVectorStore()

    def override_document_service():
        return DocumentService(
            ingestion_pipeline=IngestionPipeline(),
            embedding_model=FakeEmbedding(),
            vector_store=vector_store,
            session_id="integration-test-session",
        )

    app.dependency_overrides[get_document_service] = (
        override_document_service
    )
    monkeypatch.chdir(tmp_path)

    try:
        client = TestClient(app=app)

        upload_response = client.post(
            "api/v1/documents/upload",
            files={
                "file": (
                    "sample.txt",
                    b"RAG combines retrieval and generation.",
                    "text/plain",
                )
            }
        )

        assert upload_response.status_code == 201

        response = client.get(
            "api/v1/documents"
        )

        assert response.status_code == 200

        body = response.json()

        assert body["total"] == 1
        assert len(body["documents"]) == 1

        document = body["documents"][0]

        assert document["document_id"] == (
            upload_response.json()["document_id"]
        )
        assert document["filename"] == "sample.txt"
        assert document["chunks_count"] > 0

    finally:
        app.dependency_overrides.pop(
            get_document_service,
            None,
        )

def test_get_document_detail_through_api(tmp_path, monkeypatch):
    vector_store = FakeVectorStore()

    def override_document_service():
        return DocumentService(
            ingestion_pipeline=IngestionPipeline(),
            embedding_model=FakeEmbedding(),
            vector_store=vector_store,
            session_id="integration-test-session",
        )

    app.dependency_overrides[get_document_service] = (
        override_document_service
    )

    monkeypatch.chdir(tmp_path)

    try:
        client = TestClient(app=app)

        upload_response = client.post(
            "api/v1/documents/upload",
            files={
                "file": (
                    "sample.txt",
                    b"RAG combines retrieval and generation.",
                    "text/plain",
                )
            },
        )

        assert upload_response.status_code == 201

        document_id = upload_response.json()["document_id"]

        response = client.get(f"api/v1/documents/{document_id}")

        assert response.status_code == 200

        body = response.json()

        assert body["document_id"] == document_id
        assert body["filename"] == "sample.txt"
        assert body["chunks_count"] > 0
        assert isinstance(body["metadata"], dict)

    finally:
        app.dependency_overrides.pop(
            get_document_service,
            None,
        )

def test_delete_document_through_api(tmp_path, monkeypatch):
    vector_store = FakeVectorStore()

    def override_document_service():
        return DocumentService(
            ingestion_pipeline=IngestionPipeline(),
            embedding_model=FakeEmbedding(),
            vector_store=vector_store,
            session_id="integration-test-session",
        )

    app.dependency_overrides[get_document_service] = (
        override_document_service
    )
    monkeypatch.chdir(tmp_path)

    try:
        client = TestClient(app=app)

        upload_response = client.post(
            "/api/v1/documents/upload",
            files={
                "file": (
                    "sample.txt",
                    b"RAG combines retrieval and generation.",
                    "text/plain",
                )
            },
        )

        assert upload_response.status_code == 201
        document_id = upload_response.json()["document_id"]

        delete_response = client.delete(
            f"/api/v1/documents/{document_id}"
        )

        assert delete_response.status_code == 200
        assert delete_response.json() == {
            "document_id": document_id,
            "status": "deleted",
        }

        list_response = client.get("/api/v1/documents")

        assert list_response.status_code == 200
        assert list_response.json()["total"] == 0
        assert list_response.json()["documents"] == []

    finally:
        app.dependency_overrides.pop(
            get_document_service,
            None,
        )
