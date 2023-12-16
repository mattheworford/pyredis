from dataclasses import dataclass
from typing import Any

from src.models.resp.data_types.bulk_string import BulkString
from src.models.resp.resp_data_type import RespDataType


@dataclass
class Array(RespDataType):
    arr: list[RespDataType] | None

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
        return f"[{", ".join(str(data) for data in self.arr)}]"

    @classmethod
    def tokenize(cls, str_: str) -> "Array":
        return Array([BulkString(element) for element in str_.split()])

    def encode(self) -> bytes:
        if self.arr is None:
            return b"*-1\r\n"
        encoded_elements = b"".join([data.encode() for data in self.arr])
        return f"*{len(self.arr)}\r\n".encode() + encoded_elements
