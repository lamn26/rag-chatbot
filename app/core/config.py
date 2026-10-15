from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Local models
    LOCAL_LLM_MODEL: str = "qwen2.5:7b"
    LOCAL_EMBEDDING_MODEL: str = "qwen3-embedding:0.6b"
    LOCAL_VECTOR_SIZE: int = 1024

    # Service URLs
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    QDRANT_URL: str = "http://localhost:6333"

    # Optional cloud configuration
    API_KEY: str | None = None
    CLOUD_LLM_MODEL: str | None = None
    CLOUD_EMBEDDING_MODEL: str | None = None
    CLOUD_VECTOR_SIZE: int | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
