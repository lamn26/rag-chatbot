import uuid
from pathlib import Path
from fastapi import UploadFile

from app.ingestion.pipeline import IngestionPipeline
from app.embeddings.local import LocalEmbedding
from app.vectorstore.qdrant import QdrantVectorStore
from app.schemas.document import DocumentUploadResponse

from app.utils.hashing import calculate_sha256

from app.core.exceptions import DuplicateDocumentError

class DocumentService:
    SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".doc", ".txt"}

    def __init__(
        self,
        ingestion_pipeline: IngestionPipeline,
        embedding_model: LocalEmbedding,
        vector_store: QdrantVectorStore,
        session_id: str,
    ):
        self.ingestion_pipeline = ingestion_pipeline
        self.embedding_model = embedding_model
        self.vector_store = vector_store
        self.session_id = session_id

    async def upload_document(
        self,
        file: UploadFile,
    ) -> DocumentUploadResponse:
        temp_path = None

        try:
            if not file.filename:
                raise ValueError("Filename is required.")

            filename = Path(file.filename).name
            extension = Path(file.filename).suffix.lower()

            if extension not in self.SUPPORTED_EXTENSIONS:
                raise ValueError(
                    f"Unsupported file type: {extension}"
                )

            upload_dir = (
                Path("data/sessions")
                / self.session_id
                / "raw"
            )

            upload_dir.mkdir(parents=True, exist_ok=True)

            temp_path = upload_dir / f"{uuid.uuid4()}{extension}"

            content = await file.read()

            if not content:
                raise ValueError("Uploaded file is empty.")

            file_hash = calculate_sha256(content=content)

            if self.vector_store.check_document_exist_by_hash(
                file_hash=file_hash
            ):
                raise DuplicateDocumentError(
                    "This document has already been uploaded."
                )

            temp_path.write_bytes(content)

            chunks = self.ingestion_pipeline.process_file(
                file_path=str(temp_path)
            )

            if not chunks:
                raise ValueError(
                    "No text chunks were extracted from the document."
                )

            for chunk in chunks:
                chunk.metadata["filename"] = filename
                chunk.metadata["source"] = filename
                chunk.metadata["file_hash"] = file_hash

            texts = [chunk.content for chunk in chunks]
            embeddings = self.embedding_model.embed_documents(texts=texts)

            self.vector_store.add_documents(
                documents=chunks,
                embeddings=embeddings
            )

            document_id = chunks[0].document_id

            return DocumentUploadResponse(
                document_id=document_id,
                filename=filename,
                status="completed",
                chunks_created=len(chunks)
            )

        finally:
            if temp_path is not None and temp_path.exists():
                temp_path.unlink()
            await file.close()

    def list_documents(self):
        documents = self.vector_store.list_documents()

        return {
            "documents": documents,
            "total": len(documents)
        }

    def get_document_by_id(self, document_id: str):
        document = self.vector_store.get_document_by_id(document_id=document_id)

        if document is None:
            return None

        documents = self.vector_store.list_documents()

        for item in documents:
            if item["document_id"] == document_id:
                document["chunks_count"] = item["chunks_count"]
                break

        return document

    def delete_document(self, document_id: str) -> bool:
        document = self.vector_store.get_document_by_id(document_id=document_id)

        if document is None:
            return False

        self.vector_store.delete_document(document_id=document_id)
        return True
    