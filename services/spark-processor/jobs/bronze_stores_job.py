from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

from app.config import settings


REQUIRED_COLUMNS = {
    "store_nbr",
    "city",
    "state",
    "type",
    "cluster",
}


def validate_stores(
    dataframe: DataFrame,
) -> None:

    missing_columns = (
        REQUIRED_COLUMNS
        - set(dataframe.columns)
    )

    if missing_columns:
        raise ValueError(
            f"Missing required stores columns: "
            f"{sorted(missing_columns)}"
        )


def transform_stores_to_bronze(
    dataframe: DataFrame,
) -> DataFrame:

    validate_stores(dataframe)

    return (
        dataframe

        .withColumnRenamed(
            "type",
            "store_type",
        )

        .withColumn(
            "processed_at",
            F.current_timestamp(),
        )

        .withColumn(
            "source",
            F.lit("favorita"),
        )
    )


def write_bronze_stores(
    dataframe: DataFrame,
) -> None:

    (
        dataframe.write
        .mode("overwrite")
        .parquet(
            settings.bronze_stores_path
        )
    )


def run_bronze_stores_job(
    spark: SparkSession,
) -> None:

    raw_df = spark.read.parquet(
        settings.raw_stores_path
    )

    bronze_df = (
        transform_stores_to_bronze(
            raw_df
        )
    )

    write_bronze_stores(
        bronze_df
    )