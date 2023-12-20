import asyncio

from src.command_handler import handle_command
from src.models.data_store import DataStore
from src.models.resp.data_types.array import Array
from src.protocol_handler import extract_resp_data_and_size


class ServerProtocol(asyncio.Protocol):
    def __init__(self, data_store: DataStore) -> None:
        self._data_store = data_store
        self.transport: asyncio.BaseTransport | None = None

    def connection_made(self, transport: asyncio.BaseTransport) -> None:
        self.transport = transport

    def data_received(self, data: bytes) -> None:
        if not data:
            self.transport.close()  # type: ignore

        command_data, size = extract_resp_data_and_size(data)

        if command_data and type(command_data) is Array:
            response = handle_command(command_data, self._data_store)
            if response is not None:
                self.transport.write(response.encode())  # type: ignore
