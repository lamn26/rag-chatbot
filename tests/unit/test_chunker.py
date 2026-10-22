from unittest.mock import MagicMock, patch

from app.ingestion.chunker import DocumentChunker

@patch("app.ingestion.chunker.SemanticChunker")
@patch("app.ingestion.chunker.LocalEmbedding")
def test_document_chunker_initializes_semantic_splitter(
    mock_embedding,
    mock_semantic_chunker,
):
    chunker = DocumentChunker()

    # Assert: embedding
    mock_embedding.assert_called_once_with()

    # Assert: SemanticChunker
    mock_semantic_chunker.assert_called_once_with(
        embeddings=mock_embedding.return_value,
        breakpoint_threshold_amount=0.9,
    )

    # Assert: splitter
    assert chunker.splitter is mock_semantic_chunker.return_value


@patch("app.ingestion.chunker.SemanticChunker")
@patch("app.ingestion.chunker.LocalEmbedding")
def test_split_delegates_documents_to_semantic_splitter(
    mock_embedding,
    mock_semantic_chunker,
):
    # Arrange
    mock_splitter = mock_semantic_chunker.return_value
    documents = [MagicMock(), MagicMock()]
    expected_chunks = [MagicMock(), MagicMock()]
    mock_splitter.split_documents.return_value = expected_chunks

    chunker = DocumentChunker()

    # Act
    result = chunker.split(documents)

    # Assert
    mock_splitter.split_documents.assert_called_once_with(documents)
    assert result is expected_chunks
