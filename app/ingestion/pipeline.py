import uuid
from pathlib import Path

from app.ingestion.loader import DocumentLoader
from app.ingestion.parser import UnstructuredParser
from app.ingestion.chunker import DocumentChunker
from app.ingestion.metadata import enrich_metadata
from app.schemas.chunk import DocumentChunk

class IngestionPipeline:

    def __init__(self):

        self.loader = DocumentLoader()
        self.parser = UnstructuredParser()

        self.chunker = DocumentChunker()

    def process_file(
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

    def process_folder(
        self,
        folder_path: str,
        recursive: bool = False
    ) -> list[DocumentChunk]:
        folder = Path(folder_path)

        if not folder.exists():
            raise FileNotFoundError(
                f"Folder not found: {folder}"
            )

        if not folder.is_dir():
            raise NotADirectoryError(
                f"Not a directory: {folder}"
            )

        files = (
            folder.rglob("*")
            if recursive
            else folder.iterdir()
        )

        all_chunks = []

        for file_path in sorted(files):
            if not file_path.is_file():
                continue

            print(f"Processing: {file_path}")

            try:
                chunks = self.process_file(str(file_path))
                all_chunks.extend(chunks)

                print(f"  Created {len(chunks)} chunks.")

            except Exception as e:
                print(f"  Failed: {file_path} - {e}")

        return all_chunks