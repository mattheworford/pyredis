from typing import Any


class DataStore:
    def __init__(self) -> None:
        self._data: dict[str, Any] = dict()

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self._data[key] = value
