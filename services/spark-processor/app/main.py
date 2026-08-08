from app.spark_session import create_spark_session
from jobs.bronze_sales_job import run_bronze_sales_job
from app.config import settings

def main() -> None:

    spark = create_spark_session()

    spark.sparkContext.setLogLevel("WARN")

    try:

        print(
            "Starting RetailPulse RAW -> BRONZE pipeline..."
        )

        run_bronze_sales_job(
            spark
        )

        print(
            "RAW -> BRONZE pipeline completed successfully."
        )

        # bronze_df = spark.read.parquet(
        #     settings.bronze_sales_path
        # )

        # print("\n===== BRONZE COUNT =====")
        # print(bronze_df.count())

        # print("\n===== BRONZE SCHEMA =====")
        # bronze_df.printSchema()

        # print("\n===== BRONZE SAMPLE =====")
        # bronze_df.show(10, truncate=False)

    finally:

        spark.stop()


if __name__ == "__main__":
    main()