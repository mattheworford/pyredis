import socket

from src.command_handler import handle_command
from src.models.protocol.array import Array
from src.protocol_handler import extract_data_from_payload

RECV_SIZE = 1024


def handle_client_connection(client_socket: socket.socket) -> None:
    try:
        while True:
            payload = client_socket.recv(RECV_SIZE)

            if not payload:
                break

            command_data, size = extract_data_from_payload(payload)
            if type(command_data) is Array:
                response = handle_command(command_data)
                if response is not None:
                    client_socket.send(response.resp_encode())

    finally:
        client_socket.close()


class Server:
    _server_socket: socket.socket | None
    port: int
    _running: bool

    def __init__(self, port: int) -> None:
        self._server_socket = None
        self.port = port
        self._running = False

    def run(self) -> None:
        self._running = True

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            self._server_socket = server_socket
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_address = ("localhost", self.port)
            server_socket.bind(server_address)
            server_socket.listen()
            while self._running:
                connection, _ = server_socket.accept()
                handle_client_connection(connection)

    def stop(self) -> None:
        self._running = False
