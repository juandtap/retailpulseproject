from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # Spark
    spark_app_name: str
    spark_master: str

    # S3 / MinIO
    s3_endpoint: str
    s3_access_key: str
    s3_secret_key: str
    s3_path_style_access: bool
    s3_ssl_enabled: bool

    # Data Lake
    data_lake_bucket: str
    raw_sales_path: str
    bronze_sales_path: str


    raw_stores_path: str
    bronze_stores_path: str

    silver_sales_path: str

    # Logging
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()