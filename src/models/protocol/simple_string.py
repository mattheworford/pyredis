from dataclasses import dataclass


@dataclass
class SimpleString:
    data: str

    def resp_encode(self):
        return f"+{self.data}\r\n".encode()

    def __str__(self):
        return self.data
