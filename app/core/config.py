from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    API_KEY: str
    CLOUD_LLM_MODEL: str
    CLOUD_EMBEDDING_MODEL:str
    CLOUD_VECTOR_SIZE: int

    LOCAL_LLM_MODEL: str
    LOCAL_EMBEDDING_MODEL: str
    LOCAL_VECTOR_SIZE: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()