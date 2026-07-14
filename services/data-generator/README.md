# Data Generator

Microservice responsible for simulating a continuous stream of retail sales data.

## Responsibilities

- Read historical sales data.
- Generate configurable micro-batches.
- Upload batches to the Raw zone of the Data Lake.
- Persist processing state.

## Technologies

- Python
- Pandas
- MinIO SDK
- Pydantic Settings
- Loguru