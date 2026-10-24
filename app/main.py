from fastapi import FastAPI

from app.api.routes import (
    chat,
    documents,
    session,
    health,
)

app = FastAPI(
    title="RAG Chatbot API",
    description="A Retrieval-Augmented Generation chatbot API",
    version="0.1.0",
)

app.include_router(chat.router)
app.include_router(documents.router)
app.include_router(session.router)
app.include_router(health.router)