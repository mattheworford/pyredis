import socket

from src.command_handler import handle_command
from src.protocol_handler import extract_data_from_payload


RECV_SIZE = 1024


def handle_client_connection(client_socket):
    try:
        while True:
            payload = client_socket.recv(RECV_SIZE)

            if not payload:
                break

            command_data, size = extract_data_from_payload(payload)
            response = handle_command(command_data)
            client_socket.send(response.resp_encode())

    finally:
        client_socket.close()


class Server:
    def __init__(self, port):
        self._server_socket = None
        self.port = port
        self._running = False

    def run(self):
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

def stop(self):
        self._running = False