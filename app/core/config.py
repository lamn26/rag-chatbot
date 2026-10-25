from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    LOCAL_LLM_MODEL: str
    LOCAL_EMBEDDING_MODEL: str
    LOCAL_VECTOR_SIZE: int

    OLLAMA_BASE_URL: str
    QDRANT_URL: str

    model_config = SettingsConfigDict(
        env_file=ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
