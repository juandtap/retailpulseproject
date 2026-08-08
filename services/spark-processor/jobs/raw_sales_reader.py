from pyspark.sql import DataFrame, SparkSession

from app.config import settings


def read_raw_sales(
    spark: SparkSession,
) -> DataFrame:

    return spark.read.parquet(
        settings.raw_sales_path
    )