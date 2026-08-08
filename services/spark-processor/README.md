# RetailPulse - Spark Processor

## Overview

The Spark Processor is responsible for transforming raw datasets stored in the RetailPulse Data Lake into curated analytical datasets following the Medallion Architecture.
It reads raw Parquet files from MinIO using Apache Spark, performs distributed transformations, validates data quality, enriches datasets with technical metadata, and writes the results into the Bronze layer.

---

## Responsibilities

    -Read datasets from the Raw layer.
    -Validate dataset schema.
    -Apply distributed transformations using Apache Spark.
    -Enrich records with technical metadata.
    -Write partitioned datasets into the Bronze layer.
    -Serve as the foundation for future Silver and Gold transformations.

---

## Current Pipeline

```text
Raw Layer (MinIO)
        │
        ▼
Apache Spark
        │
        ▼
Schema Validation
        │
        ▼
Data Transformation
        │
        ▼
Technical Metadata
        │
        ▼
Bronze Layer (MinIO)
```
## Current implemented pipeline:

```
text
raw/sales
      │
      ▼
Spark Processor
      │
      ▼
bronze/sales

```
---

## Technology Stack

    -Apache Spark 4.1
    -PySpark
    -Python 3
    -Docker
    -MinIO (S3 Compatible Storage)
    -Parquet
    -Pydantic Settings
    -Loguru

---

## Project Structure

```text
spark-processor/

├── app/
│   ├── config.py
│   ├── main.py
│   ├── spark_session.py
│   └── ...
│
├── jobs/
│   ├── raw_sales_reader.py
│   ├── bronze_sales_job.py
│   └── ...
│
├── requirements.txt
├── .env.example
└── README.md

```

---

## Current Features


    -Spark Standalone Cluster
    -Distributed processing
    -MinIO integration through S3A
    -Raw dataset reader
    -Bronze Sales pipeline
    -Automatic schema validation
    -Technical metadata generation
    -Partitioned Parquet output

---


## Bronze Layer

The Bronze layer stores validated datasets while preserving the original business information.
Current transformations include:
Schema validation
Technical metadata generation
Business date normalization
Partitioning by:
    - Year
    - Month
Output example:

```

bronze/

└── sales/
    ├── year=2013/
    │   ├── month=1/
    │   ├── month=2/
    │   └── ...
    ├── year=2014/
    └── ...
```
---
## Metadata
Each processed dataset contains technical metadata used for lineage and auditing.

## Current metadata includes:

    processed_at
    source
    ingestion_year
    ingestion_month
    ingestion_day
    ingestion_hour

---


## Running the Pipeline


Start the infrastructure:
```bash
make up
make spark-up
```
Execute the Spark job:
```bash
docker exec -it \
    -w /opt/retailpulse/spark-processor \
    -e PYTHONPATH=/opt/retailpulse/spark-processor \
    retailpulse-spark-master \
    /opt/spark/bin/spark-submit \
    app/main.py
```
---
Current Data Flow

```

Corporación Favorita Dataset

        │

        ▼

Data Generator (Pandas)

        │

        ▼

Raw Layer (MinIO)

        │

        ▼

Apache Spark

        │

        ▼

Bronze Layer (MinIO)
```

---
## Roadmap

### Completed

Spark Standalone Cluster

S3A integration with MinIO

Raw Sales Reader

Bronze Sales pipeline

Distributed processing

### In Progress

Bronze Stores pipeline

Bronze Transactions pipeline

Bronze Oil pipeline

Bronze Holidays pipeline

Planned

Silver Layer

Gold Layer

Airflow orchestration

Kafka integration

Data Quality Framework

Feature Engineering

Machine Learning pipelines

Dashboard generation
