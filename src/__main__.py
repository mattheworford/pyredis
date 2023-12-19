import asyncio
from typing import Any

import typer

from src.models.data_store import DataStore
from src.models.server_protocol import ServerProtocol

_DEFAULT_PORT = 6379
_DEFAULT_HOSTNAME = "127.0.0.1"


async def flush_expired_data(data_store: DataStore) -> None:
    while True:
        data_store.flush_expired_data()
        await asyncio.sleep(0.1)


async def main(host: str = _DEFAULT_HOSTNAME, port: int = _DEFAULT_PORT) -> Any:
    print(f"Starting PyRedis on port: {port}")

    loop = asyncio.get_running_loop()

    data_store = DataStore()
    _ = loop.create_task(flush_expired_data(data_store))

    server = await loop.create_server(lambda: ServerProtocol(data_store), host, port)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    typer.run(asyncio.run(main()))
