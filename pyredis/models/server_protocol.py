import asyncio
from copy import copy, deepcopy

from pyredis.command_handler import handle_command
from pyredis.models.append_only_persister import AppendOnlyPersister
from pyredis.models.data_store import DataStore
from pyredis.models.resp.data_types.array import Array
from pyredis.models.resp.data_types.error import Error
from pyredis.protocol_handler import extract_resp_data_and_size


class ServerProtocol(asyncio.Protocol):
    def __init__(self, data_store: DataStore, persister: AppendOnlyPersister) -> None:
        self._data_store = data_store
        self._persister = persister
        self.transport: asyncio.BaseTransport | None = None

    def connection_made(self, transport: asyncio.BaseTransport) -> None:
        self.transport = transport

    def data_received(self, data: bytes) -> None:
        if not data:
            self.transport.close()  # type: ignore

        command_data, size = extract_resp_data_and_size(data)

        if command_data and isinstance(command_data, Array):
            response = handle_command(command_data, self._data_store, self._persister)
            if response is not None:
                self.transport.write(response.encode())  # type: ignore
