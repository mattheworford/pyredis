import socket

import typer
from typing_extensions import Annotated

from pyredis.models.resp.data_types.array import Array
from pyredis.protocol_handler import extract_resp_data_and_size

_DEFAULT_PORT = 6379
_DEFAULT_HOSTNAME = "127.0.0.1"
_RECV_SIZE = 1024


def _encode_command(command: str) -> bytes:
    tokenized_command = Array.tokenize(command)
    return tokenized_command.encode()


def main(
    hostname: Annotated[str, typer.Argument()] = _DEFAULT_HOSTNAME,
    port: Annotated[int, typer.Argument()] = _DEFAULT_PORT,
) -> None:
    with socket.socket() as client_socket:
        client_socket.connect((hostname, port))

        while True:
            command = input(f"{hostname}:{port}>")

            if command == "quit":
                break

            encoded_command = _encode_command(command)
            client_socket.send(encoded_command)

            while True:
                encoded_response = client_socket.recv(_RECV_SIZE)
                response, size = extract_resp_data_and_size(encoded_response)

                if response:
                    print(response)
                    break


if __name__ == "__main__":
    typer.run(main)
