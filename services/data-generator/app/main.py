from pathlib import Path

from app.builders.object_name_builder import ObjectNameBuilder
from app.config import settings
from app.generators.batch_generator import BatchGenerator
from app.logger import logger
from app.readers.sales_dataset_reader import SalesDatasetReader
from app.serializers.parquet_serializer import ParquetSerializer
from app.uploaders.minio_uploader import MinIOUploader


def main():

    logger.info("RetailPulse Data Generator started.")

    # -------------------------------------------------
    # Read dataset
    # -------------------------------------------------

    reader = SalesDatasetReader()

    reader.load()

    # -------------------------------------------------
    # Generate batch
    # -------------------------------------------------

    generator = BatchGenerator(
        dataframe=reader.dataframe,
        batch_size=settings.data_batch_size,
    )

    batch = generator.next_batch()

    logger.info(
        f"Generated batch #{batch.batch_number} "
        f"({batch.row_count} rows)"
    )

    # -------------------------------------------------
    # Serialize
    # -------------------------------------------------

    serializer = ParquetSerializer()

    output_path = Path(
        f"tmp/batch_{batch.batch_number:06}.parquet"
    )

    serializer.save(
        batch=batch,
        destination=output_path,
    )

    logger.info(f"Parquet created: {output_path}")

    # -------------------------------------------------
    # Build object name
    # -------------------------------------------------

    builder = ObjectNameBuilder()

    object_name = builder.build(batch)

    logger.info(f"Object name: {object_name}")

    # -------------------------------------------------
    # Upload
    # -------------------------------------------------

    uploader = MinIOUploader()

    uploader.upload(
        source=output_path,
        object_name=object_name,
    )

    logger.success("Pipeline completed successfully.")


if __name__ == "__main__":
    main()