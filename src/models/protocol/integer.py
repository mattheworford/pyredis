from dataclasses import dataclass


@dataclass
class Integer:
    value: int | None

    @classmethod
    def from_string(cls, data):
        try:
            value = int(data)
            return cls(value)
        except ValueError:
            return None
