from unittest.mock import MagicMock

import pytest

from app.services.document_service import DocumentService

@pytest.fixture
def document_service():
    ingestion_pipeline = MagicMock()
    embedding_model = MagicMock()
    vector_store = MagicMock()

    service = DocumentService(
        ingestion_pipeline=ingestion_pipeline,
        embedding_model=embedding_model,
        vector_store=vector_store,
        session_id="test-session",
    )

    return service, vector_store

def test_list_documents_returns_documents_and_total(document_service):
    service, vector_store = document_service

    documents = [
        {
            "document_id": "doc-001",
            "filename": "paper.pdf",
            "chunks_count": 3,
        },
        {
            "document_id": "doc-002",
            "filename": "notes.txt",
            "chunks_count": 2,
        },
    ]
    vector_store.list_documents.return_value = documents

    result = service.list_documents()

    assert result == {
        "documents": documents,
        "total": 2,
    }
    vector_store.list_documents.assert_called_once_with()

def test_list_documents_when_empty(document_service):
    service, vector_store = document_service
    vector_store.list_documents.return_value = []

    result = service.list_documents()

    assert result == {"documents": [], "total": 0}

def test_get_document_by_id_returns_none_when_not_found(
    document_service,
):
    service, vector_store = document_service
    vector_store.get_document_by_id.return_value = None

    result = service.get_document_by_id("missing-doc")

    assert result is None
    vector_store.list_documents.assert_not_called()

def test_get_document_by_id_includes_chunks_count(document_service):
    service, vector_store = document_service

    vector_store.get_document_by_id.return_value = {
        "document_id": "doc-001",
        "filename": "paper.pdf",
        "metadata": {"page_count": 5},
    }
    vector_store.list_documents.return_value = [
        {
            "document_id": "doc-001",
            "filename": "paper.pdf",
            "chunks_count": 3,
        }
    ]

    result = service.get_document_by_id("doc-001")

    assert result["document_id"] == "doc-001"
    assert result["chunks_count"] == 3
    assert result["metadata"] == {"page_count": 5}

def test_get_document_by_id_when_not_in_list(document_service):
    service, vector_store = document_service

    vector_store.get_document_by_id.return_value = {
        "document_id": "doc-001",
        "filename": "paper.pdf",
    }
    vector_store.list_documents.return_value = []

    result = service.get_document_by_id("doc-001")

    assert result == {
        "document_id": "doc-001",
        "filename": "paper.pdf",
    }

def test_delete_document_returns_false_when_not_found(
    document_service,
):
    service, vector_store = document_service
    vector_store.get_document_by_id.return_value = None

    result = service.delete_document("missing-doc")

    assert result is False
    vector_store.delete_document.assert_not_called()

def test_delete_document_deletes_existing_document(
    document_service,
):
    service, vector_store = document_service
    vector_store.get_document_by_id.return_value = {
        "document_id": "doc-001",
        "filename": "paper.pdf",
    }

    result = service.delete_document("doc-001")

    assert result is True
    vector_store.delete_document.assert_called_once_with(
        document_id="doc-001"
    )