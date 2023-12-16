from datetime import datetime
from threading import Lock

from src.models.entry import Entry


class DataStore:
    def __init__(self) -> None:
        self._data: dict[str, Entry] = dict()
        self._lock = Lock()

    def __getitem__(self, key: str) -> Entry:
        with self._lock:
            entry = self._data[key]
            if entry.expiry is not None and entry.expiry <= datetime.now():
                del self._data[key]
            return self._data[key]

    def __setitem__(self, key: str, entry: Entry) -> None:
        with self._lock:
            self._data[key] = entry

    def __delitem__(self, key: str) -> None:
        with self._lock:
            del self._data[key]
