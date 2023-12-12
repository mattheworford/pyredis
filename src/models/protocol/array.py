from dataclasses import dataclass


@dataclass
class Array:
    arr: list | None

    def resp_encode(self):
        if self.arr is None:
            return b"*-1\r\n"
        encoded_elements = b"".join([data.resp_encode() for data in self.arr])
        return f"*{len(self.arr)}\r\n".encode() + encoded_elements

    def __getitem__(self, i):
        return self.arr[i]

    def __len__(self):
        return len(self.arr)

    def __str__(self):
        return ''.join(str(data) for data in self.arr)
