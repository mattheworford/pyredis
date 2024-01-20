from dataclasses import dataclass
from typing import Any

from pyredis.models.resp.resp_data_type import RespDataType


@dataclass
class SimpleString(RespDataType):
    data: str

    def __str__(self) -> str:
        return self.data

    def encode(self) -> bytes:
        return f"+{self.data}\r\n".encode()

    def underlying(self) -> Any:
        return self.data
