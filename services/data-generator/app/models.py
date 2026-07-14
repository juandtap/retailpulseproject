from datetime import datetime

import pandas as pd
from pydantic import BaseModel, ConfigDict


class Batch(BaseModel):
    """
    Represents a micro-batch of sales data.
    """

    batch_number: int

    dataframe: pd.DataFrame

    row_count: int

    created_at: datetime

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )

class GeneratorState(BaseModel):
    """
    Stores the generator execution state.
    """

    current_index: int

    next_batch_number: int