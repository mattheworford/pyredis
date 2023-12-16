from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class Entry:
    value: Any
    expiry: datetime | None
