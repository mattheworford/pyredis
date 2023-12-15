from dataclasses import dataclass


@dataclass
class Integer:
    value: int | None

    @classmethod
    def from_string(cls, data: str) -> "Integer":
        try:
            value = int(data)
            return cls(value)
        except ValueError:
            return Integer(None)

    def resp_encode(self) -> bytes:
        return f":{self.value}\r\n".encode()

    def __str__(self) -> str:
        return str(self.value)
