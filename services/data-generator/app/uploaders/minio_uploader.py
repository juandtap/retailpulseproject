from pathlib import Path

from minio import Minio

from app.config import settings
from app.logger import logger


class MinIOUploader:

    def __init__(self):

        self._client = Minio(
            endpoint=settings.minio_endpoint,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            secure=settings.minio_secure,
        )

        self._bucket = settings.minio_bucket

    def upload(
        self,
        source: Path,
        object_name: str,
    ) -> None:
        
        logger.info(f"Uploading {object_name}")

        self._client.fput_object(
            bucket_name=self._bucket,
            object_name=object_name,
            file_path=str(source),
        )

        logger.success("Upload finished successfully.")