from dataclasses import dataclass


@dataclass
class SimpleString:
    data: str

    def resp_encode(self) -> bytes:
        return f"+{self.data}\r\n".encode()

    def __str__(self) -> str:
        return self.data
