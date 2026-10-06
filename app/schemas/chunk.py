from pydantic import BaseModel

class DocumentChunk(BaseModel):
    chunk_id: str
    document_id: str
    content: str
    metadata: dict