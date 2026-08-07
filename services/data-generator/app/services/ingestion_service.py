import time
from pathlib import Path
from datetime import UTC, datetime

from app.builders.object_name_builder import ObjectNameBuilder
from app.config import settings
from app.generators.batch_generator import BatchGenerator
from app.logger import logger
from app.models import GeneratorState
from app.readers.sales_dataset_reader import SalesDatasetReader
from app.serializers.parquet_serializer import ParquetSerializer
from app.state.state_manager import StateManager
from app.uploaders.minio_uploader import MinIOUploader


class IngestionService:

    def run(self) -> None:

        # --------------------------------------------------
        # Load dataset
        # --------------------------------------------------

        reader = SalesDatasetReader()
        reader.load()

        # --------------------------------------------------
        # Load state
        # --------------------------------------------------

        state_manager = StateManager(settings.state_file)

        state = state_manager.load()

        logger.info(
            f"Last uploaded batch: {state.last_uploaded_batch}"
        )

        processed_rows = state.last_uploaded_rows

        # --------------------------------------------------
        # Create pipeline components
        # --------------------------------------------------

        generator = BatchGenerator(
            dataframe=reader.dataframe,
            batch_size=settings.data_batch_size,
            start_batch=state.last_uploaded_batch + 1,
        )

        serializer = ParquetSerializer()

        uploader = MinIOUploader()

        builder = ObjectNameBuilder()

        # --------------------------------------------------
        # Process batches
        # --------------------------------------------------

        while generator.has_next():

            batch = generator.next_batch()

            logger.info(
                f"Processing batch #{batch.batch_number}"
            )

            
            output_path = Path(
                settings.tmp_directory
            ) / f"batch_{batch.batch_number:06}.parquet"

            serializer.save(
                batch=batch,
                destination=output_path
            )
            logger.info(
                f"Parquet created: {output_path}"
            )

            object_name = builder.build(batch)

            uploader.upload(
                source=output_path,
                object_name=object_name,
            )

            processed_rows += batch.row_count

            state = GeneratorState(
                last_uploaded_batch=batch.batch_number,
                last_uploaded_rows=processed_rows,
                last_uploaded_at=datetime.now(UTC),
            )

            state_manager.save(state)

            logger.info(
                f"State saved (batch {batch.batch_number})"
            )

            if output_path.exists():

                output_path.unlink()

                logger.info(
                    f"Temporary file deleted: {output_path.name}"
                )

            time.sleep(
                settings.data_batch_interval
            )

        logger.success(
            "Dataset fully processed."
        )