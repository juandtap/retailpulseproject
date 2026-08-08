from pyspark.sql import SparkSession

from app.config import settings


def create_spark_session() -> SparkSession:

    spark = (
        SparkSession.builder
        .appName(settings.spark_app_name)
        .master(settings.spark_master)
        
        # Driver Host
        .config(
            "spark.driver.host",
            "spark-master",
        )
        .config(
            "spark.driver.bindAddress",
            "0.0.0.0",
        )


        # S3A implementation
        .config(
            "spark.hadoop.fs.s3a.impl",
            "org.apache.hadoop.fs.s3a.S3AFileSystem",
        )

        # MinIO endpoint
        .config(
            "spark.hadoop.fs.s3a.endpoint",
            settings.s3_endpoint,
        )

        # Credentials
        .config(
            "spark.hadoop.fs.s3a.access.key",
            settings.s3_access_key,
        )
        .config(
            "spark.hadoop.fs.s3a.secret.key",
            settings.s3_secret_key,
        )

        # Needed by MinIO / S3-compatible storage
        .config(
            "spark.hadoop.fs.s3a.path.style.access",
            str(settings.s3_path_style_access).lower(),
        )

        # Local development: no HTTPS
        .config(
            "spark.hadoop.fs.s3a.connection.ssl.enabled",
            str(settings.s3_ssl_enabled).lower(),
        )

        # Explicit credentials provider
        .config(
            "spark.hadoop.fs.s3a.aws.credentials.provider",
            "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider",
        )

        .getOrCreate()
    )

    return spark