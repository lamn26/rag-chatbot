from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="Question asked by the user",
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Maximum number of chunks to retrieve",
    )

    score_threshold: float = Field(
        default=0.825,
        ge=0.0,
        le=1.0,
        description="Minimum similarity score for retrieval",
    )


class SourceItem(BaseModel):
    filename: str | None = None
    page_number: int | str | None = None
    chunk_index: int | None = None
    score: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceItem]
