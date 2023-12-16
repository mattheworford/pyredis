from dataclasses import dataclass

from src.models.resp.resp_data_type import RespDataType


@dataclass
class BulkString(RespDataType):
    data: str | None

    def __str__(self) -> str:
        return self.data or ""

    def encode(self) -> bytes:
        if self.data is None:
            return b"$-1\r\n"
        return f"${len(self.data)}\r\n{self.data}\r\n".encode()
