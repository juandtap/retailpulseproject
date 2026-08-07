from pathlib import Path

from app.models import GeneratorState


class StateManager:

    def __init__(
        self,
        state_file: str,
    ):

        self._state_file = Path(state_file)

    def load(self) -> GeneratorState:

        if not self._state_file.exists():

            return GeneratorState()

        return GeneratorState.model_validate_json(
            self._state_file.read_text(
                encoding="utf-8"
            )
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
            state.model_dump_json(indent=4),
            encoding="utf-8",
        )