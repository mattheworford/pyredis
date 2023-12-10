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