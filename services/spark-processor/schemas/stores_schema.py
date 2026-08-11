from pyspark.sql.types import (
    ShortType,
    StringType,
    StructField,
    StructType,
)


STORES_SCHEMA = StructType(
    [
        StructField(
            "store_nbr",
            ShortType(),
            nullable=False,
        ),
        StructField(
            "city",
            StringType(),
            nullable=False,
        ),
        StructField(
            "state",
            StringType(),
            nullable=False,
        ),
        StructField(
            "type",
            StringType(),
            nullable=False,
        ),
        StructField(
            "cluster",
            ShortType(),
            nullable=False,
        ),
    ]
)