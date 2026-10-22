import pytest
from pydantic import ValidationError

from app.schemas.document import (
    Document,
    DocumentUploadResponse,
    DocumentListItem,
    DocumentListResponse,
    DocumentDetailResponse,
    DocumentDeleteResponse,
)
from app.schemas.chunk import DocumentChunk

VALID_SCHEMA_DATA = [
    (
        Document,
        {
            "document_id": "doc-001",
            "filename": "paper.pdf",
            "content": "Transformer architecture",
            "metadata": {"page_count": 10},
        },
    ),
    (
        DocumentUploadResponse,
        {
            "document_id": "doc-001",
            "filename": "paper.pdf",
            "status": "success",
            "chunks_created": 20,
        },
    ),
    (
        DocumentListItem,
        {
            "document_id": "doc-001",
            "filename": "paper.pdf",
            "chunks_count": 20,
        },
    ),
    (
        DocumentListResponse,
        {
            "documents": [
                {
                    "document_id": "doc-001",
                    "filename": "paper.pdf",
                    "chunks_count": 20,
                }
            ],
            "total": 1,
        },
    ),
    (
        DocumentDetailResponse,
        {
            "document_id": "doc-001",
            "filename": "paper.pdf",
            "chunks_count": 20,
            "metadata": {"page_count": 10},
        },
    ),
    (
        DocumentDeleteResponse,
        {
            "document_id": "doc-001",
            "status": "deleted",
        },
    ),
    (
        DocumentChunk,
        {
            "chunk_id": "chunk-001",
            "document_id": "doc-001",
            "content": "Attention is all you need.",
            "metadata": {"page_number": 1},
        },
    ),
]

@pytest.mark.parametrize("schema, data", VALID_SCHEMA_DATA)
def test_schema_accepts_valid_data(schema, data):
    instance = schema(**data)

    assert isinstance(instance, schema)


@pytest.mark.parametrize("schema, data", VALID_SCHEMA_DATA)
def test_schema_rejects_missing_required_field(schema, data):
    incomplete_data = data.copy()
    missing_field = next(iter(data))
    incomplete_data.pop(missing_field)

    with pytest.raises(ValidationError):
        schema(**incomplete_data)

def test_document_preserves_content_and_metadata():
    document = Document(
        document_id="doc-001",
        filename="paper.pdf",
        content="Transformer architecture",
        metadata={"page_count": 10},
    )

    assert document.content == "Transformer architecture"
    assert document.metadata == {"page_count": 10}

def test_document_accepts_empty_metadata():
    document = Document(
        document_id="doc-001",
        filename="paper.pdf",
        content="Some content",
        metadata={},
    )

    assert document.metadata == {}

def test_document_list_response_parses_nested_documents():
    response = DocumentListResponse(
        documents=[
            {
                "document_id": "doc-001",
                "filename": "paper.pdf",
                "chunks_count": 20,
            }
        ],
        total=1,
    )

    assert len(response.documents) == 1
    assert isinstance(response.documents[0], DocumentListItem)
    assert response.documents[0].document_id == "doc-001"