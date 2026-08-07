from datetime import datetime, UTC

from pandas import DataFrame
from pydantic import BaseModel, ConfigDict, Field


class Batch(BaseModel):
    """
    Represents a micro-batch of sales data.
    """

    batch_number: int

    dataframe: DataFrame

    row_count: int

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )

class GeneratorState(BaseModel):
    """
    Stores the generator execution state.
    """
    last_uploaded_batch: int = 0
    last_uploaded_rows: int = 0
    last_uploaded_at: datetime | None = None