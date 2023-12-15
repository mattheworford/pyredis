from dataclasses import dataclass


@dataclass
class Error:
    type: str
    message: str

    @classmethod
    def from_string(cls, data: str) -> "Error":
        first, _, rest = data.partition(" ")
        if first.isupper():
            return cls(first, rest or "")
        else:
            return cls("", data)

    @classmethod
    def wrong_arg_num(cls, command: str) -> "Error":
        message = f"wrong number of arguments for '{command}' command"
        return cls("ERR", message)

    def resp_encode(self) -> bytes:
        return f"-{str(self)}\r\n".encode()

    def __str__(self) -> str:
        return self.type + " " + self.message if len(self.type) > 0 else self.message
