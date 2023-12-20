from dataclasses import dataclass
from typing import Any

from src.models.resp.resp_data_type import RespDataType


@dataclass
class Error(RespDataType):
    type: str
    message: str

    def __str__(self) -> str:
        return " ".join(
            [self.type, self.message if len(self.type) > 0 else self.message]
        )

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


@dataclass
class NumberOfArgumentsError(Error):
    def __init__(self, command: str) -> None:
        self.type = "ERR"
        self.message = f"wrong number of arguments for '{command}' command"


@dataclass
class WrongValueTypeError(Error):
    def __init__(self) -> None:
        self.type = "WRONGTYPE"
        self.message = "Operation against a key holding the wrong kind of value"


@dataclass
class NonIntOrOutOfRangeError(Error):
    def __init__(self) -> None:
        self.type = "ERR"
        self.message = "value is not an integer or out of range"
