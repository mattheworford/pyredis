from dataclasses import dataclass

from src.models.resp.resp_data_type import RespDataType


@dataclass
class SimpleString(RespDataType):
    data: str

    def __str__(self) -> str:
        return self.data

    def encode(self) -> bytes:
        return f"+{self.data}\r\n".encode()
