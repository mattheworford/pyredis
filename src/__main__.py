import asyncio
from typing import Any

import typer

from src.models.server import Server

REDIS_DEFAULT_HOST = "127.0.0.1"
REDIS_DEFAULT_PORT = 6379


async def main(host: str = REDIS_DEFAULT_HOST, port: int = REDIS_DEFAULT_PORT) -> Any:
    print(f"Starting PyRedis on port: {port}")
    loop = asyncio.get_running_loop()

    server = await loop.create_server(lambda: Server(), host, port)

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    typer.run(asyncio.run(main()))
