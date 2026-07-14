from app.config import settings
from app.models import Batch


class ObjectNameBuilder:

    def build(self, batch: Batch) -> str:

        date = batch.dataframe.iloc[0]["date"]

        return (
            f"{settings.raw_sales_prefix}/"
            f"year={date.year}/"
            f"month={date.month:02}/"
            f"day={date.day:02}/"
            f"batch_{batch.batch_number:06}.parquet"
        )