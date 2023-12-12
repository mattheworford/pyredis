import pytest

from src.command_handler import handle_command
from src.models.protocol.array import Array
from src.models.protocol.bulk_string import BulkString
from src.models.protocol.error import Error
from src.models.protocol.simple_string import SimpleString


@pytest.mark.parametrize(
    "command, expected",
    [
        # PING Tests
        (Array([BulkString("PING")]), SimpleString("PONG")),
        (Array([BulkString("PING"), BulkString("Hello")]), BulkString("Hello")),
        # ECHO Tests
        (
                Array([BulkString("ECHO")]),
                Error("ERR", "wrong number of arguments for 'echo' command"),
        ),
        (Array([BulkString("ECHO"), BulkString("Hello")]), BulkString("Hello")),
        (
                Array([BulkString("echo"), BulkString("Hello"), BulkString("World")]),
                Error("ERR", "wrong number of arguments for 'echo' command"),
        ),
    ],
)
def test_handle_command(command, expected):
    result = handle_command(command)
    assert result == expected
