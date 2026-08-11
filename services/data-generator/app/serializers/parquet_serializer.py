from pathlib import Path

import pandas as pd


class ParquetSerializer:

    def save(
        self,
        dataframe: pd.DataFrame,
        destination: Path,
    ) -> None:

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        dataframe.to_parquet(
            destination,
            index=False,
            engine="pyarrow",
        )