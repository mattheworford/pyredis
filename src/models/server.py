import asyncio
import socket

from src.command_handler import handle_command
from src.models.data_store import DataStore
from src.models.protocol.array import Array
from src.protocol_handler import extract_data_from_payload

RECV_SIZE = 1024
_DATA_STORE = DataStore()


class Server(asyncio.Protocol):
    def __init__(self) -> None:
        self.transport: asyncio.BaseTransport | None = None
        self.buffer = bytearray()

    def connection_made(self, transport: asyncio.BaseTransport) -> None:
        self.transport = transport

    def data_received(self, data: bytes) -> None:
        if type(self.transport) is asyncio.WriteTransport:
            if not data:
                self.transport.close()

            self.buffer.extend(data)

            command_data, size = extract_data_from_payload(self.buffer)

            if command_data and type(command_data) is Array:
                self.buffer = self.buffer[size:]
                response = handle_command(command_data, _DATA_STORE)
                if response is not None:
                    self.transport.write(response.resp_encode())
