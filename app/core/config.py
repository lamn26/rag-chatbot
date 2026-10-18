from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    # Local models
    LOCAL_LLM_MODEL: str
    LOCAL_EMBEDDING_MODEL: str
    LOCAL_VECTOR_SIZE: int

    # Service URLs
    OLLAMA_BASE_URL: str
    QDRANT_URL: str

    # Optional cloud configuration
    API_KEY: str
    CLOUD_LLM_MODEL: str
    CLOUD_EMBEDDING_MODEL: str
    CLOUD_VECTOR_SIZE: int

    model_config = SettingsConfigDict(
        env_file=ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
