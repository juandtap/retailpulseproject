from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

from app.config import settings


def validate_store_keys(
    sales_df: DataFrame,
    stores_df: DataFrame,
) -> None:

    missing_stores = (
        sales_df
        .select("store_nbr")
        .distinct()
        .join(
            stores_df.select("store_nbr"),
            on="store_nbr",
            how="left_anti",
        )
    )

    missing_count = missing_stores.count()

    if missing_count > 0:
        raise ValueError(
            f"Found {missing_count} store keys "
            f"without matching store metadata."
        )


def transform_to_silver(
    sales_df: DataFrame,
    stores_df: DataFrame,
) -> DataFrame:

    validate_store_keys(
        sales_df,
        stores_df,
    )

    sales = sales_df.alias("sales")
    stores = stores_df.alias("stores")

    silver_df = (
        sales
        .join(
            F.broadcast(stores),
            on="store_nbr",
            how="left",
        )
        .select(
            # Business identifiers
            F.col("sales.id").alias("id"),
            F.col("sales.sale_date").alias("sale_date"),
            F.col("store_nbr"),

            # Store dimensions
            F.col("stores.city").alias("city"),
            F.col("stores.state").alias("state"),
            F.col("stores.store_type").alias("store_type"),
            F.col("stores.cluster").alias("cluster"),

            # Sales data
            F.col("sales.family").alias("family"),
            F.col("sales.sales").alias("sales"),
            F.col("sales.onpromotion").alias("onpromotion"),

            # Original sales ingestion metadata
            F.col("sales.ingestion_year").alias(
                "ingestion_year"
            ),
            F.col("sales.ingestion_month").alias(
                "ingestion_month"
            ),
            F.col("sales.ingestion_day").alias(
                "ingestion_day"
            ),
            F.col("sales.ingestion_hour").alias(
                "ingestion_hour"
            ),

            # Business partitions
            F.col("sales.year").alias("year"),
            F.col("sales.month").alias("month"),
        )
        .withColumn(
            "silver_processed_at",
            F.current_timestamp(),
        )
    )

    return silver_df

def write_silver_sales(
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
            settings.silver_sales_path
        )
    )


def run_silver_sales_job(
    spark: SparkSession,
) -> None:

    sales_df = spark.read.parquet(
        settings.bronze_sales_path
    )

    stores_df = spark.read.parquet(
        settings.bronze_stores_path
    )

    silver_df = transform_to_silver(
        sales_df,
        stores_df,
    )

    validate_silver_sales(
        silver_df
    )

    silver_df.explain(mode="formatted")

    write_silver_sales(
        silver_df
    )


def validate_silver_sales(dataframe: DataFrame) -> None:

    null_store_metadata = (
        dataframe
        .filter(
            F.col("city").isNull()
            | F.col("state").isNull()
            | F.col("store_type").isNull()
            | F.col("cluster").isNull()
        )
        .count()
    )

    if null_store_metadata > 0:
        raise ValueError(
            f"Found {null_store_metadata} rows "
            "with missing store metadata."
        )

    duplicate_ids = (
        dataframe
        .groupBy("id")
        .count()
        .filter(F.col("count") > 1)
        .count()
    )

    if duplicate_ids > 0:
        raise ValueError(
            f"Found {duplicate_ids} duplicated sales IDs."
        )

    invalid_sales = (
        dataframe
        .filter(F.col("sales") < 0)
        .count()
    )

    if invalid_sales > 0:
        raise ValueError(
            f"Found {invalid_sales} rows with negative sales."
        )