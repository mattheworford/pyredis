import typer

from src.models.server import Server

REDIS_DEFAULT_PORT = 6379


def main(port: int = REDIS_DEFAULT_PORT) -> None:
    print(f"Starting PyRedis on port: {port}")
    server = Server(port)
    server.run()


if __name__ == "__main__":
    typer.run(main)
