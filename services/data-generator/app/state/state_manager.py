from pathlib import Path

from app.models import GeneratorState

from datetime import datetime

from pydantic import BaseModel


class GeneratorState(BaseModel):

    last_uploaded_batch: int = 0

    last_uploaded_rows: int = 0

    last_uploaded_at: datetime | None = None


class StateManager:

    def __init__(self, state_file: str):

        self._state_file = Path(state_file)

    def load(self) -> GeneratorState:

        if not self._state_file.exists():

            return GeneratorState()

        return GeneratorState.model_validate_json(
            self._state_file.read_text()
        )

    def save(
        self,
        state: GeneratorState,
    ) -> None:

        self._state_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._state_file.write_text(
            state.model_dump_json(indent=4)
        )