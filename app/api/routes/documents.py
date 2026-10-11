from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)

from app.api.dependencies import get_document_service
from app.schemas.document import (
    DocumentUploadResponse,
    DocumentListResponse,
    DocumentDetailResponse,
    DocumentDeleteResponse,
)
from app.services.document_service import DocumentService

from app.core.exceptions import DuplicateDocumentError

router = APIRouter(
    prefix="/api/v1/documents",
    tags=["Documents"],
)

@router.post(
    "/upload",
    response_model=DocumentUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    file: UploadFile = File(...),
    document_service: DocumentService = Depends(get_document_service),
) -> DocumentUploadResponse:
    try:
        return await document_service.upload_document(file=file)
    except DuplicateDocumentError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e

@router.get(
    "",
    response_model=DocumentListResponse
)
def list_documents(
    document_service: DocumentService = Depends(
        get_document_service
    ),
) -> DocumentListResponse:
    return document_service.list_documents()

@router.get(
    "/{document_id}",
    response_model=DocumentDetailResponse,
)
def get_document_by_id(
    document_id: str,
    document_service: DocumentService = Depends(
        get_document_service
    ),
) -> DocumentDetailResponse:
    document = document_service.get_document_by_id(
        document_id=document_id
    )

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    return document

@router.delete(
    "/{document_id}",
    response_model=DocumentDeleteResponse,
)
def delete_document(
    document_id: str,
    document_service: DocumentService = Depends(
        get_document_service
    )
) -> DocumentDeleteResponse:
    deleted = document_service.delete_document(
        document_id=document_id
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    return DocumentDeleteResponse(
        document_id=document_id,
        status="deleted",
    )

