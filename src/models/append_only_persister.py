from src.models.resp.data_types.array import Array


class AppendOnlyPersister:
    def __init__(self, filename: str) -> None:
        self._filename = filename
        self._file = open(filename, mode="ab", buffering=0)

    def log_command(self, command: Array) -> None:
        self._file.write(f"*{len(command)}\r\n".encode())

        for item in command:
            self._file.write(item.encode())
