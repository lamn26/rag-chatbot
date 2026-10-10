import uuid
from pathlib import Path
from fastapi import UploadFile

from app.ingestion.pipeline import IngestionPipeline
from app.embeddings.local import LocalEmbedding
from app.vectorstore.qdrant import QdrantVectorStore
from app.schemas.document import DocumentUploadResponse

class DocumentService:
    SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".doc", ".txt"}

    def __init__(
        self,
        ingestion_pipeline: IngestionPipeline,
        embedding_model: LocalEmbedding,
        vector_store: QdrantVectorStore,
    ):
        self.ingestion_pipeline = ingestion_pipeline
        self.embedding_model = embedding_model
        self.vector_store = vector_store

    async def upload_document(
        self,
        file: UploadFile,
    ) -> DocumentUploadResponse:
        if not file.filename:
            raise ValueError("Filename is required.")

        filename = Path(file.filename).name
        extension = Path(file.filename).suffix.lower()

        if extension not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: {extension}"
            )

        upload_dir = Path("data/raw")
        upload_dir.mkdir(parents=True, exist_ok=True)

        temp_path = upload_dir / f"{uuid.uuid4()}{extension}"

        try:
            content = await file.read()

            if not content:
                raise ValueError("Uploaded file is empty.")

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
            if temp_path.exists():
                temp_path.unlink()
            await file.close()