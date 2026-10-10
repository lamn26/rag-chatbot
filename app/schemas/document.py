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

class DocumentListItem(BaseModel):
    document_id: str
    filename: str
    chunks_count: int


class DocumentListResponse(BaseModel):
    documents: list[DocumentListItem]
    total: int

class DocumentDetailResponse(BaseModel):
    document_id: str
    filename: str
    chunks_count: int
    metadata: dict

class DocumentDeleteResponse(BaseModel):
    document_id: str
    status: str