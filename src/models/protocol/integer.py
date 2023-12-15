from dataclasses import dataclass


@dataclass
class Integer:
    value: int

    @classmethod
    def from_string(cls, data: str):  # type: ignore
        try:
            value = int(data)
            return cls(value)
        except ValueError:
            return None

    def resp_encode(self) -> bytes:
        return f":{self.value}\r\n".encode()

    def __str__(self) -> str:
        return str(self.value)
