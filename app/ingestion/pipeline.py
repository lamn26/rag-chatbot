import uuid

from app.ingestion.loader import DocumentLoader
from app.ingestion.parser import UnstructuredParser
from app.ingestion.chunker import DocumentChunker
from app.schemas.chunk import DocumentChunk

class IngestionPipeline:

    def __init__(self):

        self.loader = DocumentLoader()
        self.parser = UnstructuredParser()

        self.chunker = DocumentChunker(
            chunk_size=1200,
            chunk_overlap=200,
        )

    def process(
        self,
        file_path: str,
    ) -> list[DocumentChunk]:

        path = self.loader.load(file_path)

        documents = self.parser.parse(path)

        chunks = self.chunker.split(
            documents
        )

        document_id = str(uuid.uuid4())

        results = []

        for chunk in chunks:

            chunk_id = str(uuid.uuid4())

            metadata = dict(
                chunk.metadata
            )

            metadata["document_id"] = document_id

            results.append(
                DocumentChunk(
                    chunk_id=chunk_id,
                    document_id=document_id,
                    content=chunk.page_content,
                    metadata=metadata,
                )
            )

        return results