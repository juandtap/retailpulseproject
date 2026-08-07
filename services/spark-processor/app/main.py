from app.config import settings
from app.spark_session import create_spark_session
from jobs.raw_sales_reader import read_raw_sales


def main() -> None:

    spark = create_spark_session()

    try:

        df = read_raw_sales(spark)

        print("\n===== SCHEMA =====")
        df.printSchema()

        print("\n===== SAMPLE =====")
        df.show(10, truncate=False)

        print("\n===== COUNT =====")
        print(df.count())

    finally:

        spark.stop()


if __name__ == "__main__":
    main()