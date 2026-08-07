from app.config import settings
from app.models import Batch


class ObjectNameBuilder:

    def build(self, batch: Batch) -> str:

        ingestion_time = batch.created_at

        return (
            f"{settings.raw_sales_prefix}/"
            f"ingestion_year={ingestion_time.year}/"
            f"ingestion_month={ingestion_time.month:02}/"
            f"ingestion_day={ingestion_time.day:02}/"
            f"ingestion_hour={ingestion_time.hour:02}/"
            f"batch_{batch.batch_number:06}.parquet"
        )