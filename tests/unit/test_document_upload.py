from unittest.mock import MagicMock

import pytest
from fastapi import UploadFile
from io import BytesIO

from app.services.document_service import DocumentService
from app.schemas.document import DocumentUploadResponse
from app.core.exceptions import DuplicateDocumentError

@pytest.fixture
def anyio_backend():
    return "asyncio"

@pytest.fixture
def upload_service(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    ingestion_pipeline = MagicMock()
    embedding_model = MagicMock()
    vector_store = MagicMock()

    service = DocumentService(
        ingestion_pipeline=ingestion_pipeline,
        embedding_model=embedding_model,
        vector_store=vector_store,
        session_id="test-session",
    )

    return service, ingestion_pipeline, embedding_model, vector_store


def make_upload_file(
    filename="paper.txt",
    content=b"Sample document content",
):
    return UploadFile(
        filename=filename,
        file=BytesIO(content),
    )


@pytest.mark.anyio
async def test_upload_document_rejects_missing_filename(upload_service):
    service, _, _, _ = upload_service
    file = make_upload_file(filename="")

    with pytest.raises(ValueError, match="Filename is required."):
        await service.upload_document(file)

    assert file.file.closed


@pytest.mark.anyio
async def test_upload_document_rejects_unsupported_extension(upload_service):
    service, _, _, _ = upload_service
    file = make_upload_file(filename="image.png")

    with pytest.raises(ValueError, match="Unsupported file type"):
        await service.upload_document(file)

    assert file.file.closed


@pytest.mark.anyio
async def test_upload_document_rejects_empty_file(upload_service):
    service, _, _, _ = upload_service
    file = make_upload_file(content=b"")

    with pytest.raises(ValueError, match="Uploaded file is empty."):
        await service.upload_document(file)

    assert file.file.closed


@pytest.mark.anyio
async def test_upload_document_rejects_duplicate(upload_service):
    service, _, _, vector_store = upload_service
    vector_store.check_document_exist_by_hash.return_value = True

    file = make_upload_file()

    with pytest.raises(DuplicateDocumentError):
        await service.upload_document(file)

    vector_store.add_documents.assert_not_called()
    assert file.file.closed


@pytest.mark.anyio
async def test_upload_document_rejects_when_no_chunks_extracted(
    upload_service,
):
    service, ingestion_pipeline, _, vector_store = upload_service
    ingestion_pipeline.process_file.return_value = []
    vector_store.check_document_exist_by_hash.return_value = False

    file = make_upload_file()

    with pytest.raises(
        ValueError,
        match="No text chunks were extracted from the document.",
    ):
        await service.upload_document(file)

    vector_store.add_documents.assert_not_called()
    assert file.file.closed


@pytest.mark.anyio
async def test_upload_document_success(upload_service):
    service, ingestion_pipeline, embedding_model, vector_store = upload_service

    chunk = MagicMock()
    chunk.content = "Sample document content"
    chunk.document_id = "doc-001"
    chunk.metadata = {}

    ingestion_pipeline.process_file.return_value = [chunk]
    embedding_model.embed_documents.return_value = [[0.1, 0.2]]
    vector_store.check_document_exist_by_hash.return_value = False

    file = make_upload_file(
        filename="paper.txt",
        content=b"Sample document content",
    )

    result = await service.upload_document(file)

    assert isinstance(result, DocumentUploadResponse)
    assert result.document_id == "doc-001"
    assert result.filename == "paper.txt"
    assert result.status == "completed"
    assert result.chunks_created == 1

    assert chunk.metadata["filename"] == "paper.txt"
    assert chunk.metadata["source"] == "paper.txt"
    assert "file_hash" in chunk.metadata

    embedding_model.embed_documents.assert_called_once_with(
        texts=["Sample document content"]
    )
    vector_store.add_documents.assert_called_once_with(
        documents=[chunk],
        embeddings=[[0.1, 0.2]],
    )

    assert file.file.closed