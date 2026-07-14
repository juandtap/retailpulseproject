from pathlib import Path

from app.models import Batch


class ParquetSerializer:

    def save(
        self,
        batch: Batch,
        destination: Path,
    ) -> None:

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        batch.dataframe.to_parquet(
            destination,
            index=False,
            engine="pyarrow",
        )