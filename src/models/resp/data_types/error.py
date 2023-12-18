from dataclasses import dataclass
from typing import Any

from src.models.resp.resp_data_type import RespDataType


@dataclass
class Error(RespDataType):
    type: str
    message: str

    def __str__(self) -> str:
        return self.type + " " + self.message if len(self.type) > 0 else self.message

    def encode(self) -> bytes:
        return f"-{str(self)}\r\n".encode()

    def underlying(self) -> Any:
        return str(self)

    @classmethod
    def from_string(cls, data: str) -> "Error":
        first, _, rest = data.partition(" ")
        if first.isupper():
            return cls(first, rest or "")
        else:
            return cls("", data)

    @classmethod
    def get_arg_num_error(cls, command: str) -> "Error":
        message = f"wrong number of arguments for '{command}' command"
        return cls("ERR", message)
