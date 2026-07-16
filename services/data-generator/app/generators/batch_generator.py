from pandas import DataFrame

from app.models import Batch


class BatchGenerator:

    def __init__(
        self,
        dataframe: DataFrame,
        batch_size: int,
        start_batch: int = 1,
    ) -> None:

        self._dataframe = dataframe
        self._batch_size = batch_size

        self._batch_number = start_batch

        self._current_index = (
            start_batch - 1
        ) * batch_size

    def has_next(self) -> bool:

        return self._current_index < len(self._dataframe)

    def next_batch(self) -> Batch:

        if not self.has_next():
            raise StopIteration("No more batches available.")

        start = self._current_index

        end = min(
            start + self._batch_size,
            len(self._dataframe),
        )

        batch_dataframe = self._dataframe.iloc[start:end]

        batch = Batch(
            batch_number=self._batch_number,
            dataframe=batch_dataframe,
            row_count=len(batch_dataframe),
        )

        self._current_index = end

        self._batch_number += 1

        return batch