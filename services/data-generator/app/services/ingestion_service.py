import time

from datetime import UTC, datetime
from pathlib import Path

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

        # -----------------------------
        # Read Dataset
        # -----------------------------

        reader = SalesDatasetReader()

        reader.load()


        ## load state

        state_manager = StateManager(
                settings.state_file
            )

        state = state_manager.load()

        logger.info(
            f"Last uploaded batch: {state.last_uploaded_batch}"
        )

        # -----------------------------
        # Generate Batch
        # -----------------------------

        generator = BatchGenerator(
            dataframe=reader.dataframe,
            batch_size=settings.data_batch_size,
            start_batch=state.last_uploaded_batch + 1,
        )

        while generator.has_next():

            batch = generator.next_batch()

            logger.info(
                f"Generated batch #{batch.batch_number} "
                f"({batch.row_count} rows)"
            )

            # -----------------------------
            # Serialize
            # -----------------------------

            serializer = ParquetSerializer()

            output_path = Path(
                f"tmp/batch_{batch.batch_number:06}.parquet"
            )

            serializer.save(
                batch=batch,
                destination=output_path,
            )

            # -----------------------------
            # Build Object Name
            # -----------------------------

            builder = ObjectNameBuilder()

            object_name = builder.build(batch)

            logger.info(f"Object Name: {object_name}")

            # -----------------------------
            # Upload
            # -----------------------------

            uploader = MinIOUploader()

            uploader.upload(
                source=output_path,
                object_name=object_name,
            )

            # save state

            state = GeneratorState(
                last_uploaded_batch=batch.batch_number,
                last_uploaded_rows=batch.batch_number * settings.data_batch_size,
                last_uploaded_at=datetime.now(UTC),
            )

            state_manager.save(state)

            logger.info(
                f"State saved (batch {batch.batch_number})"
            )

            if output_path.exists():

                output_path.unlink()

                logger.info(
                    f"Deleted temporary file: {output_path.name}"
                )

            time.sleep(
                settings.data_batch_interval
            )

        logger.success("Pipeline completed successfully.")