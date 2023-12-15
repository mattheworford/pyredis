from dataclasses import dataclass


@dataclass
class Error:
    type: str
    message: str

    @classmethod
    def from_string(cls, data: str):  # type: ignore
        first, _, rest = data.partition(" ")
        if first.isupper():
            return cls(first, rest or "")
        else:
            return cls("", data)

    def resp_encode(self) -> bytes:
        return f"-{str(self)}\r\n".encode()

    def __str__(self) -> str:
        return self.type + " " + self.message if len(self.type) > 0 else self.message
