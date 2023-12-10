from dataclasses import dataclass


@dataclass
class Array:
    data: list | None

    def resp_encode(self):
        if self.data is None:
            return b"*-1\r\n"
        encoded_elements = b"".join([data.resp_encode() for data in self.data])
        return f"*{len(self.data)}\r\n".encode() + encoded_elements
