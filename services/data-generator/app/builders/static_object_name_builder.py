from datetime import UTC, datetime

from app.config import settings


class StaticObjectNameBuilder:

    def build_stores(self) -> str:

        ingestion_time = datetime.now(UTC)

        return (
            f"{settings.raw_stores_prefix}/"
            f"ingestion_year={ingestion_time.year}/"
            f"ingestion_month={ingestion_time.month:02}/"
            f"ingestion_day={ingestion_time.day:02}/"
            f"stores.parquet"
        )