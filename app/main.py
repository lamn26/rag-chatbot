# import asyncio

# from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.routes import (
    chat,
    documents,
    session,
)

# from app.core.session_manager import session_manager

# async def cleanup_expired_sessions():
#     while True:
#         await asyncio.sleep(15)
#
#         try:
#             session_manager.cleanup_expired_sessions()
#         except Exception as e:
#             print(f"[SESSION CLEANUP] Error during cleanup: {e}")
#
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     cleanup_task = asyncio.create_task(
#         cleanup_expired_sessions()
#     )
#
#     try:
#         yield
#     finally:
#         cleanup_task.cancel()
#
#         try:
#             await cleanup_task
#         except asyncio.CancelledError:
#             pass

app = FastAPI(
    title="RAG Chatbot API",
    description="A Retrieval-Augmented Generation chatbot API",
    version="0.1.0",
    # lifespan=lifespan
)

app.include_router(chat.router)
app.include_router(documents.router)
app.include_router(session.router)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}