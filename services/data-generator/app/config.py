from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration loaded from .env
    """

    # Data Generator
    data_batch_size: int
    data_batch_interval: int

    # Dataset
    train_dataset_path: str

    # MinIO
    minio_endpoint: str
    minio_access_key: str
    minio_secret_key: str
    minio_bucket: str
    minio_secure: bool

    # Logs
    log_level: str

    #local 
    state_file: str

    tmp_directory: str

    # Object naming
    raw_sales_prefix: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    stores_dataset_path: str
    raw_stores_prefix: str


@lru_cache
def get_settings() -> Settings:
    """
    Load settings once (Singleton).
    """
    return Settings()


settings = get_settings()