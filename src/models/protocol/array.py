from dataclasses import dataclass
from typing import Any

from src.models.protocol.bulk_string import BulkString
from src.models.protocol.error import Error
from src.models.protocol.integer import Integer
from src.models.protocol.simple_string import SimpleString


@dataclass
class Array:
    arr: list[Any] | None

    def resp_encode(self) -> bytes:
        if self.arr is None:
            return b"*-1\r\n"
        encoded_elements = b"".join([data.resp_encode() for data in self.arr])
        return f"*{len(self.arr)}\r\n".encode() + encoded_elements

    def __getitem__(self, i: int | slice) -> Any:
        if self.arr is None:
            return None
        return self.arr[i]

    def __len__(self) -> int:
        if self.arr is None:
            return 0
        return len(self.arr)

    def __str__(self) -> str:
        if self.arr is None:
            return ""
        return "".join(str(data) for data in self.arr)
