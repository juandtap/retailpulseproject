from app.spark_session import create_spark_session
from jobs.bronze_sales_job import (
    run_bronze_sales_job,
)
from jobs.bronze_stores_job import (
    run_bronze_stores_job,
)

from jobs.silver_sales_job import (
    run_silver_sales_job,
)

from app.config import settings

def main() -> None:

    spark = create_spark_session()

    spark.sparkContext.setLogLevel("WARN")

    try:

        print(
            "Starting RetailPulse Bronze pipelines..."
        )

        print(
            "\n[1/3] Processing sales..."
        )

        run_bronze_sales_job(
            spark
        )

        print(
            "\n[2/3] Processing stores..."
        )

        run_bronze_stores_job(
            spark
        )

        print(
            "\nBronze pipelines completed successfully."
        )

        print(
            "\n[3/3] Processing Silver Sales..."
        )

        run_silver_sales_job(
            spark
        )

        print(
            "\Silver pipelines completed successfully."
        )

        print("TEST SILVER SALES_STORES....")
        
        silver_df = spark.read.parquet(
            settings.silver_sales_path
        )

        silver_df.printSchema()

        silver_df.show(
            10,
            truncate=False,
        )

        print(
            f"Silver stores sales: {silver_df.count()}"
        )

        print("TEST BRONZE SALES....")
        
        stores_df = spark.read.parquet(
            settings.bronze_sales_path
        )

        stores_df.printSchema()

        stores_df.show(
            10,
            truncate=False,
        )

        print(
            f"Bronze stores sales: {stores_df.count()}"
        )
        

    finally:

        spark.stop()


if __name__ == "__main__":
    main()