import collections
from dataclasses import dataclass
from typing import Any, Iterator

from pyredis.models.resp.data_types.bulk_string import BulkString
from pyredis.models.resp.data_types.integer import Integer
from pyredis.models.resp.resp_data_type import RespDataType


@dataclass
class Array(RespDataType):
    arr: collections.deque[RespDataType] | None

    def __getitem__(self, i: int) -> Any:
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
        elements = "\n".join([f'{i}) "{str(data)}"' for i, data in enumerate(self.arr)])
        return f"[{elements}]"

    def __iter__(self) -> Iterator[RespDataType]:
        return iter(self.arr or [])

    @classmethod
    def tokenize(cls, str_: str) -> "Array":
        split = str_.split()
        return Array(
            collections.deque(
                [BulkString(element) for element in split], maxlen=len(split)
            )
        )

    @classmethod
    def from_list(cls, list_: list[RespDataType]) -> "Array":
        return Array(collections.deque(list_))

    def encode(self) -> bytes:
        if self.arr is None:
            return b"*-1\r\n"
        encoded_elements = b"".join([data.encode() for data in self.arr])
        return f"*{len(self.arr)}\r\n".encode() + encoded_elements

    def underlying(self) -> Any:
        return self.arr

    def popleft(self) -> RespDataType:
        if self.arr is None:
            return BulkString(None)
        return self.arr.popleft()
