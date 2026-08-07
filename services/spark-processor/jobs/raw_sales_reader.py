from pyspark.sql import SparkSession

from app.config import settings


def read_raw_sales(
    spark: SparkSession,
):
    return spark.read.parquet(
        settings.raw_sales_path
    )