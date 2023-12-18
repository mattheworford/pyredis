from dataclasses import dataclass
from typing import Any


class RespDataType:
    def encode(self) -> bytes:
        raise NotImplementedError

    def underlying(self) -> Any:
        raise NotImplementedError
