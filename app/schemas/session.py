from pydantic import BaseModel

class SessionCreateResponse(BaseModel):
    session_id: str
    collection_name: str
    status: str

class SessionEndResponse(BaseModel):
    session_id: str
    status: str
