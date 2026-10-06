from pydantic import BaseModel

class Document(BaseModel):
    document_id: str
    filename: str
    content: str
    metadata: dict