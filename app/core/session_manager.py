import shutil

from pathlib import Path
from uuid import uuid4

from app.vectorstore.qdrant import QdrantVectorStore
from app.core.config import settings

VECTOR_SIZE = settings.LOCAL_VECTOR_SIZE
SESSION_ROOT = Path("data/sessions")

class SessionManager:
    def __init__(self):
        self.active_sessions: dict[str, str] = {}

    def create_session(self) -> dict:
        session_id = uuid4().hex
        collection_name = f"rag_session_{session_id}"

        vector_store = QdrantVectorStore(
            collection_name=collection_name
        )

        vector_store.create_collection(
            vector_size=VECTOR_SIZE
        )

        session_dir = SESSION_ROOT / session_id
        session_dir.mkdir(parents=True, exist_ok=True)

        self.active_sessions[session_id] = collection_name

        print(
            f"[CREATE] manager_id={id(self)} "
            f"session_id={session_id} "
            f"active_sessions={list(self.active_sessions.keys())}"
        )

        return {
            "session_id": session_id,
            "collection_name": collection_name,
            "status": "active",
        }

    def get_collection_name(self, session_id: str) -> str:
        print(
            f"[LOOKUP] manager_id={id(self)} "
            f"session_id={session_id} "
            f"active_sessions={list(self.active_sessions.keys())}"
        )

        collection_name = self.active_sessions.get(session_id)

        if collection_name is None:
            raise ValueError("Session not found or already ended.")

        return collection_name

    def end_session(self, session_id: str) -> bool:
        collection_name = self.get_collection_name(
            session_id=session_id
        )

        vector_store = QdrantVectorStore(
            collection_name=collection_name
        )

        vector_store.delete_collection()

        session_dir = SESSION_ROOT / session_id

        if session_dir.exists():
            shutil.rmtree(session_dir)

        del self.active_sessions[session_id]

        return True

session_manager = SessionManager()