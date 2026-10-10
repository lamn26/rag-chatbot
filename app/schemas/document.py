from pydantic import BaseModel

class Document(BaseModel):
    document_id: str
    filename: str
    content: str
    metadata: dict

class DocumentUploadResponse(BaseModel):
    document_id: str
    filename: str
    status: str
    chunks_created: int