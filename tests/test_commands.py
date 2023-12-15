import pytest

from src.command_handler import handle_command
from src.models.data_store import DataStore
from src.models.protocol.array import Array
from src.models.protocol.bulk_string import BulkString
from src.models.protocol.error import Error
from src.models.protocol.simple_string import SimpleString

DATA_STORE = DataStore()


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
        # SET Tests
        (
            Array([BulkString("SET")]),
            Error("ERR", "wrong number of arguments for 'set' command"),
        ),
        (
            Array([BulkString("set"), SimpleString("key")]),
            Error("ERR", "wrong number of arguments for 'set' command"),
        ),
        (
            Array([BulkString("set"), SimpleString("key"), SimpleString("value")]),
            SimpleString("OK"),
        ),
        # GET Tests
        (
            Array([BulkString("GET")]),
            Error("ERR", "wrong number of arguments for 'get' command"),
        ),
        (
            Array([BulkString("get"), SimpleString("key"), SimpleString("value")]),
            Error("ERR", "wrong number of arguments for 'get' command"),
        ),
        (
            Array([BulkString("get"), SimpleString("key")]),
            BulkString("value"),
        ),
        (
            Array([BulkString("get"), SimpleString("non-existent")]),
            SimpleString(""),
        ),
    ],
)
def test_handle_command(
    command: Array, expected: SimpleString | Error | BulkString
) -> None:
    result = handle_command(command, DATA_STORE)
    assert result == expected
