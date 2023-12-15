import socket

import typer
from typing_extensions import Annotated

from src.models.protocol.array import Array
from src.models.protocol.bulk_string import BulkString
from src.protocol_handler import extract_data_from_payload

DEFAULT_PORT = 6378
DEFAULT_SERVER = "127.0.0.1"
RECV_SIZE = 1024


def encode_command(command: str) -> bytes:
    as_array = Array([BulkString(element) for element in command.split()])
    return as_array.resp_encode()


def main(
    server: Annotated[str, typer.Argument()] = DEFAULT_SERVER,
    port: Annotated[int, typer.Argument()] = DEFAULT_PORT,
) -> None:
    with socket.socket() as client_socket:
        client_socket.connect((server, port))
        stream = bytearray()
        while True:
            command = input(f"{server}:{port}>")

            if command == "quit":
                break

            encoded_command = encode_command(command)
            client_socket.send(encoded_command)

            while True:
                payload = client_socket.recv(RECV_SIZE)
                stream.extend(payload)
                data, size = extract_data_from_payload(stream)

                if data:
                    stream = stream[size:]
                    print(data)
                    break


if __name__ == "__main__":
    typer.run(main)
