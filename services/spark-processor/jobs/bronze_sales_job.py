from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

from app.config import settings


REQUIRED_COLUMNS = {
    "id",
    "date",
    "store_nbr",
    "family",
    "sales",
    "onpromotion",
}


def validate_schema(dataframe: DataFrame) -> None:
    missing_columns = REQUIRED_COLUMNS - set(dataframe.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )


def transform_raw_to_bronze(
    dataframe: DataFrame,
) -> DataFrame:

    validate_schema(dataframe)

    bronze_df = (
        dataframe

        # Business date
        .withColumnRenamed(
            "date",
            "sale_date",
        )

        # Technical metadata
        .withColumn(
            "processed_at",
            F.current_timestamp(),
        )
        .withColumn(
            "source",
            F.lit("favorita"),
        )

        # Business date partitions
        .withColumn(
            "year",
            F.year("sale_date"),
        )
        .withColumn(
            "month",
            F.month("sale_date"),
        )
        .withColumn(
            "day",
            F.dayofmonth("sale_date"),
        )
    )

    return bronze_df


def write_bronze_sales(
    dataframe: DataFrame,
) -> None:

    (
        dataframe.write
        .mode("overwrite")
        .partitionBy(
            "year",
            "month",
        )
        .parquet(
            settings.bronze_sales_path
        )
    )


def run_bronze_sales_job(
    spark: SparkSession,
) -> None:

    raw_df = spark.read.parquet(
        settings.raw_sales_path
    )

    bronze_df = transform_raw_to_bronze(
        raw_df
    )

    write_bronze_sales(
        bronze_df
    )