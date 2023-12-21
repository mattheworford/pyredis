import asyncio
from typing import Any

import typer

from src.command_handler import handle_command
from src.models.data_store import DataStore
from src.models.resp.data_types.error import Error
from src.models.server_protocol import ServerProtocol
from src.models.append_only_persister import AppendOnlyPersister
from src.protocol_handler import extract_resp_data_and_size

_DEFAULT_PORT = 6379
_DEFAULT_HOSTNAME = "127.0.0.1"
_DEFAULT_PERSISTENCE_FILE = "db.aof"


async def flush_expired_data(data_store: DataStore) -> None:
    while True:
        data_store.flush_expired_data()
        await asyncio.sleep(1)


def restore_from_file(filename, datastore):
    buffer = bytearray()

    with open(filename, "rb") as file:
        for line in file:
            buffer.extend(line)
        while len(buffer) > 0:
            command_data, size = extract_resp_data_and_size(buffer)
            if command_data:
                buffer = buffer[size:]
                response = handle_command(command_data, datastore, None)
                if isinstance(response, Error):
                    return False
    return True


async def main(
    host: str = _DEFAULT_HOSTNAME,
    port: int = _DEFAULT_PORT,
    persistence_file: str = _DEFAULT_PERSISTENCE_FILE,
) -> Any:
    print(f"Starting PyRedis on port: {port}")

    loop = asyncio.get_running_loop()

    data_store = DataStore()
    if not restore_from_file(persistence_file, data_store):
        return -1

    persister = AppendOnlyPersister(persistence_file)

    _ = loop.create_task(flush_expired_data(data_store))

    server = await loop.create_server(
        lambda: ServerProtocol(data_store, persister), host, port
    )
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    typer.run(asyncio.run(main()))
