import requests

from config import (
    DOCUMENT_API_URL,
    REQUEST_TIMEOUT,
    UPLOAD_TIMEOUT,
)

def upload_document(session_id: str, uploaded_file) -> dict:
    response = requests.post(
        url=f"{DOCUMENT_API_URL}/upload",
        headers={"X-Session-ID": session_id},
        files={
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type or "application/octet-stream",
            )
        },
        timeout=UPLOAD_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()

def list_documents(session_id: str) -> dict:
    response = requests.get(
        url=DOCUMENT_API_URL,
        headers={"X-Session-ID": session_id},
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()

def delete_document(session_id: str, document_id: str) -> None:
    response = requests.delete(
        url=f"{DOCUMENT_API_URL}/{document_id}",
        headers={"X-Session-ID": session_id},
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
