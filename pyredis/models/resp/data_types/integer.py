from dataclasses import dataclass
from typing import Any

from pyredis.models.resp.resp_data_type import RespDataType


@dataclass
class Integer(RespDataType):
    value: int | None

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def from_string(cls, data: str) -> "Integer":
        try:
            value = int(data)
            return cls(value)
        except ValueError:
            return Integer(None)

    def encode(self) -> bytes:
        return f":{self.value}\r\n".encode()

    def underlying(self) -> Any:
        return self.value
