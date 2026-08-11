from pathlib import Path

import pandas as pd

from app.config import settings
from app.logger import logger


class StoresDatasetReader:

    def __init__(self) -> None:

        self._dataset_path = Path(
            settings.stores_dataset_path
        )

    def load(self) -> pd.DataFrame:

        logger.info(
            f"Loading stores dataset: {self._dataset_path}"
        )

        if not self._dataset_path.exists():
            raise FileNotFoundError(
                f"Stores dataset not found: {self._dataset_path}"
            )

        dataframe = pd.read_csv(
            self._dataset_path,
            dtype={
                "store_nbr": "int16",
                "city": "category",
                "state": "category",
                "type": "category",
                "cluster": "int16",
            },
        )

        logger.info(
            f"Stores dataset loaded successfully "
            f"({len(dataframe):,} rows)"
        )

        return dataframe