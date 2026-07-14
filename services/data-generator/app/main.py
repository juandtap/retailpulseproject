from app.config import settings
from app.logger import logger
from app.readers.sales_dataset_reader import SalesDatasetReader
from app.generators.batch_generator import BatchGenerator

def main():

    logger.info("Data Generator starting...")

    #dev
    logger.info(f"Settings: ")

    logger.info(f"Batch size: {settings.data_batch_size}")

    logger.info(f"Batch interval: {settings.data_batch_interval}")

    logger.info(f"Dataset path: {settings.train_dataset_path}")

    logger.info(f"MinIO bucket: {settings.minio_bucket}")

    logger.info("Configuration loaded successfully.")

    logger.info("Starting Data Generator")


    reader = SalesDatasetReader()

    reader.load()

    generator = BatchGenerator(
        dataframe=reader.dataframe,
        batch_size=settings.data_batch_size,
    )

    batch = generator.next_batch()

    logger.info(f"Batch number: {batch.batch_number}")

    logger.info(f"Rows: {batch.row_count}")

    logger.info(batch.dataframe.head())

if __name__ == "__main__":
    main()