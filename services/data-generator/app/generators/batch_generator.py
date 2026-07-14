from __future__ import annotations
from datetime import datetime

import pandas as pd
from app.models import Batch

class BatchGenerator:

    def __init__(
        self,
        dataframe: pd.DataFrame,
        batch_size: int,
    ):

        self._dataframe = dataframe

        self._batch_size = batch_size

        self._current_index = 0

        self._batch_number = 1

    def has_next(self) -> bool:

        return self._current_index < len(self._dataframe)

    def next_batch(self) -> Batch:

        if not self.has_next():

            raise StopIteration(
                "No more batches available."
            )

        start = self._current_index

        end = start + self._batch_size

        dataframe = self._dataframe.iloc[start:end]

        batch = Batch(
            batch_number=self._batch_number,
            dataframe=dataframe,
            row_count=len(dataframe),
            created_at=datetime.now(),
        )

        self._current_index = end

        self._batch_number += 1


        return batch