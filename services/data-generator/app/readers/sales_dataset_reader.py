from pathlib import Path

import pandas as pd

from app.config import settings
from app.logger import logger


class SalesDatasetReader:
    """
    Reads the historical sales dataset into memory.
    """

    def __init__(self):

        self._dataset_path = Path(settings.train_dataset_path)

        self._dataframe: pd.DataFrame | None = None

    def load(self) -> None:

        logger.info(f"Loading dataset: {self._dataset_path}")

        if not self._dataset_path.exists():

            raise FileNotFoundError(
                f"Dataset not found: {self._dataset_path}"
            )

        self._dataframe = pd.read_csv(self._dataset_path)

        logger.info(
            f"Dataset loaded successfully ({len(self._dataframe):,} rows)"
        )

    @property
    def dataframe(self) -> pd.DataFrame:

        if self._dataframe is None:

            raise RuntimeError(
                "Dataset has not been loaded."
            )

        return self._dataframe