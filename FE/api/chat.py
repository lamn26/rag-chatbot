import requests
from config import REQUEST_TIMEOUT, CHAT_API_URL

def ask_question(
    session_id: str,
    question: str,
    top_k: int = 10,
    score_threshold: float = 0.0,
) -> dict:
    response = requests.post(
        url=CHAT_API_URL,
        headers={
            "X-Session-ID": session_id
        },
        json={
            "question": question,
            "top_k": top_k,
            "score_threshold": score_threshold,
        },
        timeout=REQUEST_TIMEOUT
    )

    response.raise_for_status()
    return response.json()