from copy import deepcopy
from dataclasses import dataclass
from typing import Any


class RespDataType:
    def encode(self) -> bytes:
        raise NotImplementedError

    def underlying(self) -> Any:
        raise NotImplementedError

    def __deepcopy__(self, memo):  # type: ignore
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result
