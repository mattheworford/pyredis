import random
from datetime import datetime, timezone
from threading import Lock

from pyredis.models.entry import Entry


class DataStore:
    def __init__(self) -> None:
        self._data: dict[str, Entry] = dict()
        self._lock = Lock()

    def __getitem__(self, key: str) -> Entry:
        with self._lock:
            entry = self._data[key]
            if entry.expiry is not None and entry.expiry <= datetime.now(timezone.utc):
                del self._data[key]
            return self._data[key]

    def __setitem__(self, key: str, entry: Entry) -> None:
        with self._lock:
            self._data[key] = entry

    def __delitem__(self, key: str) -> None:
        with self._lock:
            del self._data[key]

    def __str__(self) -> str:
        return f"{self._data}"

    def __contains__(self, key: str) -> bool:
        try:
            return self[key] is not None
        except KeyError:
            return False

    def get(self, key: str, default: Entry) -> Entry:
        if key in self:
            return self[key]
        else:
            return default

    def flush_expired_data(self) -> None:
        percent_expired: float = 1
        while percent_expired > 0.25 and len(self._data) > 0:
            sample_size = min(len(self._data), 20)
            sample: list[str] = random.sample(list(self._data.keys()), sample_size)
            num_expired = len([key for key in sample if key not in self])
            percent_expired = float(num_expired) / float(sample_size)
            print(percent_expired)
