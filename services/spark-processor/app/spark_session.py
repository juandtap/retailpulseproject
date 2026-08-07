from pyspark.sql import SparkSession

from app.config import settings


def create_spark_session() -> SparkSession:

    spark = (
        SparkSession.builder
        .appName(settings.spark_app_name)
        .master(settings.spark_master)

        .config(
            "spark.hadoop.fs.s3a.endpoint",
            settings.s3_endpoint,
        )
        .config(
            "spark.hadoop.fs.s3a.access.key",
            settings.s3_access_key,
        )
        .config(
            "spark.hadoop.fs.s3a.secret.key",
            settings.s3_secret_key,
        )
        .config(
            "spark.hadoop.fs.s3a.path.style.access",
            str(settings.s3_path_style_access).lower(),
        )
        .config(
            "spark.hadoop.fs.s3a.connection.ssl.enabled",
            str(settings.s3_ssl_enabled).lower(),
        )
        .getOrCreate()
    )

    return spark