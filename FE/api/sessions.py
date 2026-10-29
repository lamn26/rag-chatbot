import requests

from config import REQUEST_TIMEOUT, SESSION_API_URL

def create_session() -> dict:
    response = requests.post(
        url=SESSION_API_URL,
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def delete_session(session_id: str) -> None:
    response = requests.delete(
        url=f"{SESSION_API_URL}/{session_id}",
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
