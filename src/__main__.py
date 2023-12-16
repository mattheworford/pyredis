import asyncio
from typing import Any

import typer

from src.models.data_store import DataStore
from src.models.server import Server

_DEFAULT_PORT = 6379
_DEFAULT_HOSTNAME = "127.0.0.1"


async def check_expiries(data_store: DataStore) -> None:
    while True:
        data_store.check_expiries()
        await asyncio.sleep(0.1)


async def main(host: str = _DEFAULT_HOSTNAME, port: int = _DEFAULT_PORT) -> Any:
    print(f"Starting PyRedis on port: {port}")
    data_store = DataStore()
    loop = asyncio.get_running_loop()
    task = loop.create_task(check_expiries(data_store))
    server = await loop.create_server(lambda: Server(data_store), host, port)

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    typer.run(asyncio.run(main()))
