from threading import Lock
from typing import Any


class DataStore:
    def __init__(self) -> None:
        self._data: dict[str, Any] = dict()
        self._lock = Lock()

    def __getitem__(self, key: str) -> Any:
        with self._lock:
            return self._data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        with self._lock:
            self._data[key] = value
