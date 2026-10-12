from fastapi import (
    APIRouter,
    HTTPException,
    status,
)

from app.core.session_manager import session_manager
from app.schemas.session import (
    SessionCreateResponse,
    SessionEndResponse,
)

router = APIRouter(
    prefix="/api/v1/sessions",
    tags=["Sessions"],
)

@router.post(
    "",
    response_model=SessionCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_session() -> SessionCreateResponse:
    session = session_manager.create_session()

    return SessionCreateResponse(**session)

@router.delete(
    "/{session_id}",
    response_model=SessionEndResponse,
)
def end_session(session_id: str) -> SessionEndResponse:
    try:
        session_manager.end_session(
            session_id=session_id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e

    return SessionEndResponse(
        session_id=session_id,
        status="ended",
    )

# @router.post(
#     "/{session_id}/heartbeat"
# )
# def session_heartbeat(
#     session_id: str
# ) -> dict:
#     try:
#         session_manager.heartbeat(session_id)
#     except ValueError as e:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=str(e),
#         ) from e
#
#     return {"session_id": session_id, "status": "active"}