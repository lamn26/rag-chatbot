import shutil
# import time

from pathlib import Path
from uuid import uuid4

from app.vectorstore.qdrant import QdrantVectorStore
from app.core.config import settings

# SESSION_TIMEOUT_SECONDS = 90
VECTOR_SIZE = settings.LOCAL_VECTOR_SIZE
SESSION_ROOT = Path("data/sessions")

class SessionManager:
    def __init__(self):
        self.active_sessions: dict[str, str] = {}
        # self.last_seen: dict[str, float] = {}

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
        # self.last_seen[session_id] = time.time()

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
        # self.last_seen.pop(session_id, None)

        return True

    # def heartbeat(self, session_id: str) -> None:
    #     self.get_collection_name(session_id)
    #     self.last_seen[session_id] = time.time()
    #
    # def cleanup_expired_sessions(self) -> None:
    #     now = time.time()
    #
    #     expired_sessions = [
    #         session_id
    #         for session_id, last_seen in self.last_seen.items()
    #         if now - last_seen > SESSION_TIMEOUT_SECONDS
    #     ]
    #
    #     for session_id in expired_sessions:
    #         try:
    #             self.end_session(session_id)
    #             print(f"[SESSION CLEANUP] Ended session: {session_id}")
    #         except Exception as e:
    #             print(
    #                 f"[SESSION CLEANUP] Failed for "
    #                 f"{session_id}: {e}"
    #             )

session_manager = SessionManager()