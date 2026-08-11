from pathlib import Path

from app.builders.static_object_name_builder import (
    StaticObjectNameBuilder,
)
from app.config import settings
from app.logger import logger
from app.readers.stores_dataset_reader import (
    StoresDatasetReader,
)
from app.serializers.parquet_serializer import (
    ParquetSerializer,
)
from app.uploaders.minio_uploader import MinIOUploader


class StaticIngestionService:

    def run_stores(self) -> None:

        logger.info(
            "Starting stores static ingestion."
        )

        reader = StoresDatasetReader()

        dataframe = reader.load()

        serializer = ParquetSerializer()

        output_path = Path(
            settings.tmp_directory
        ) / "stores.parquet"

        serializer.save(
            dataframe=dataframe,
            destination=output_path,
        )

        builder = StaticObjectNameBuilder()

        object_name = builder.build_stores()

        uploader = MinIOUploader()

        uploader.upload(
            source=output_path,
            object_name=object_name,
        )

        if output_path.exists():
            output_path.unlink()

        logger.success(
            "Stores static ingestion completed."
        )