from dataclasses import dataclass


@dataclass
class Error:
    type: str
    message: str

    @classmethod
    def from_string(cls, data):
        first, _, rest = data.partition(" ")
        if first.isupper():
            return cls(first, rest or "")
        else:
            return cls("", data)

    def resp_encode(self):
        return f"-{str(self)}\r\n".encode()

    def __str__(self):
        return self.type + " " + self.message if len(self.type) > 0 else self.message

class WrongNumberOfArgumentsError(Error):
    def __init__(self, command):
        self.type = "ERR"
        self.message = f"wrong number of arguments for '{command}' command"
