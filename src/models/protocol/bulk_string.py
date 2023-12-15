from dataclasses import dataclass


@dataclass
class BulkString:
    data: str | None

    def resp_encode(self) -> bytes:
        if self.data is None:
            return b"$-1\r\n"
        return f"${len(self.data)}\r\n{self.data}\r\n".encode()

    def __str__(self) -> str:
        return self.data or ""
