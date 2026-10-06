import uuid

from app.ingestion.loader import DocumentLoader
from app.ingestion.parser import UnstructuredParser
from app.ingestion.chunker import DocumentChunker
from app.ingestion.metadata import enrich_metadata
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

        # 1. Validate file
        path = self.loader.load(file_path)

        # 2. Parse document
        documents = self.parser.parse(path)

        # 3. Split document into chunks
        chunks = self.chunker.split(
            documents
        )

        document_id = str(uuid.uuid4())

        results = []

        for chunk_index, chunk in enumerate(chunks):

            chunk_id = str(uuid.uuid4())

            metadata = enrich_metadata(
                metadata=chunk.metadata,
                file_path=path,
                chunk_index=chunk_index,
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