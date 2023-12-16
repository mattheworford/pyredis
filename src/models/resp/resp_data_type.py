from dataclasses import dataclass
from typing import Any


class RespDataType:
    def encode(self) -> bytes:
        raise NotImplementedError(
            f"'{type(self).__name__}.encode()' is missing implementation."
        )
