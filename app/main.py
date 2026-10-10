from fastapi import FastAPI

from app.api.routes import (
    chat,
    documents,
)

app = FastAPI(
    title="RAG Chatbot API",
    description="A Retrieval-Augmented Generation chatbot API",
    version="0.1.0",
)

app.include_router(chat.router)
app.include_router(documents.router)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}