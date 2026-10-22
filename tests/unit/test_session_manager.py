from unittest.mock import MagicMock, patch

import pytest

from app.core.session_manager import SessionManager

@pytest.fixture
def manager(tmp_path):
    session_manager = SessionManager()

    with patch(
        "app.core.session_manager.SESSION_ROOT",
        tmp_path,
    ):
        yield session_manager, tmp_path


@patch("app.core.session_manager.QdrantVectorStore")
def test_create_session(mock_vector_store, manager):
    session_manager, session_root = manager

    result = session_manager.create_session()

    session_id = result["session_id"]
    collection_name = result["collection_name"]

    assert result["status"] == "active"
    assert collection_name == f"rag_session_{session_id}"

    assert (
        session_manager.active_sessions[session_id]
        == collection_name
    )

    assert (session_root / session_id).is_dir()

    mock_vector_store.assert_called_once_with(
        collection_name=collection_name
    )
    mock_vector_store.return_value.create_collection.assert_called_once()


@patch("app.core.session_manager.QdrantVectorStore")
def test_create_multiple_sessions_generates_unique_ids(
    mock_vector_store,
    manager,
):
    session_manager, _ = manager

    first = session_manager.create_session()
    second = session_manager.create_session()

    assert first["session_id"] != second["session_id"]
    assert first["collection_name"] != second["collection_name"]
    assert len(session_manager.active_sessions) == 2


def test_get_collection_name_for_existing_session(manager):
    session_manager, _ = manager

    session_manager.active_sessions["session-001"] = (
        "rag_session_session-001"
    )

    result = session_manager.get_collection_name("session-001")

    assert result == "rag_session_session-001"


def test_get_collection_name_for_unknown_session_raises_error(
    manager,
):
    session_manager, _ = manager

    with pytest.raises(
        ValueError,
        match="Session not found or already ended.",
    ):
        session_manager.get_collection_name("unknown-session")


@patch("app.core.session_manager.QdrantVectorStore")
def test_end_session_deletes_collection_directory_and_registration(
    mock_vector_store,
    manager,
):
    session_manager, session_root = manager

    session_id = "session-001"
    collection_name = "rag_session_session-001"
    session_dir = session_root / session_id

    session_dir.mkdir(parents=True)
    (session_dir / "example.txt").write_text(
        "temporary data",
        encoding="utf-8",
    )
    session_manager.active_sessions[session_id] = collection_name

    result = session_manager.end_session(session_id)

    assert result is True

    mock_vector_store.assert_called_once_with(
        collection_name=collection_name
    )
    mock_vector_store.return_value.delete_collection.assert_called_once()

    assert not session_dir.exists()
    assert session_id not in session_manager.active_sessions


@patch("app.core.session_manager.QdrantVectorStore")
def test_end_session_without_directory_still_succeeds(
    mock_vector_store,
    manager,
):
    session_manager, _ = manager

    session_id = "session-001"
    session_manager.active_sessions[session_id] = (
        "rag_session_session-001"
    )

    result = session_manager.end_session(session_id)

    assert result is True
    mock_vector_store.return_value.delete_collection.assert_called_once()
    assert session_id not in session_manager.active_sessions


def test_end_unknown_session_raises_error(manager):
    session_manager, _ = manager

    with pytest.raises(
        ValueError,
        match="Session not found or already ended.",
    ):
        session_manager.end_session("unknown-session")
