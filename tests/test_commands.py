import time
from datetime import datetime

import pytest

from src.command_handler import handle_command
from src.models.data_store import DataStore
from src.models.resp.data_types.array import Array
from src.models.resp.data_types.bulk_string import BulkString
from src.models.resp.data_types.error import Error
from src.models.resp.data_types.integer import Integer
from src.models.resp.data_types.simple_string import SimpleString

_DATA_STORE = DataStore()


@pytest.mark.parametrize(
    "command, expected",
    [
        # PING Tests
        (Array.from_list([BulkString("PING")]), SimpleString("PONG")),
        (
            Array.from_list([BulkString("PING"), BulkString("Hello")]),
            BulkString("Hello"),
        ),
        # ECHO Tests
        (
            Array.from_list([BulkString("ECHO")]),
            Error("ERR", "wrong number of arguments for 'echo' command"),
        ),
        (
            Array.from_list([BulkString("ECHO"), BulkString("Hello")]),
            BulkString("Hello"),
        ),
        (
            Array.from_list(
                [BulkString("echo"), BulkString("Hello"), BulkString("World")]
            ),
            Error("ERR", "wrong number of arguments for 'echo' command"),
        ),
        # SET Tests
        (
            Array.from_list([BulkString("SET")]),
            Error("ERR", "wrong number of arguments for 'set' command"),
        ),
        (
            Array.from_list([BulkString("set"), BulkString("key")]),
            Error("ERR", "wrong number of arguments for 'set' command"),
        ),
        (
            Array.from_list(
                [BulkString("set"), BulkString("key"), BulkString("value")]
            ),
            SimpleString("OK"),
        ),
        (
            Array.from_list(
                [BulkString("set"), BulkString("different_key"), BulkString("value")]
            ),
            SimpleString("OK"),
        ),
        (
            Array.from_list(
                [BulkString("set"), BulkString("int_key_1"), BulkString("1")]
            ),
            SimpleString("OK"),
        ),
        # SET EX Tests
        (
            Array.from_list(
                [
                    BulkString("set"),
                    BulkString("expiring"),
                    BulkString("value"),
                    BulkString("EX"),
                ]
            ),
            Error("ERR", "wrong number of arguments for 'set' command"),
        ),
        (
            Array.from_list(
                [
                    BulkString("set"),
                    BulkString("expiring"),
                    BulkString("value"),
                    BulkString("EX"),
                    BulkString("10"),
                ]
            ),
            SimpleString("OK"),
        ),
        # SET PX Tests
        (
            Array.from_list(
                [
                    BulkString("set"),
                    BulkString("expiring"),
                    BulkString("value"),
                    BulkString("PX"),
                ]
            ),
            Error("ERR", "wrong number of arguments for 'set' command"),
        ),
        (
            Array.from_list(
                [
                    BulkString("set"),
                    BulkString("expiring"),
                    BulkString("value"),
                    BulkString("PX"),
                    BulkString("10"),
                ]
            ),
            SimpleString("OK"),
        ),
        # SET EXAT Tests
        (
            Array.from_list(
                [
                    BulkString("set"),
                    BulkString("expiring"),
                    BulkString("value"),
                    BulkString("EXAT"),
                ]
            ),
            Error("ERR", "wrong number of arguments for 'set' command"),
        ),
        (
            Array.from_list(
                [
                    BulkString("set"),
                    BulkString("expiring"),
                    BulkString("value"),
                    BulkString("EXAT"),
                    BulkString("1702701458"),
                ]
            ),
            SimpleString("OK"),
        ),
        # SET EX Tests
        (
            Array.from_list(
                [
                    BulkString("set"),
                    BulkString("expiring"),
                    BulkString("value"),
                    BulkString("PXAT"),
                ]
            ),
            Error("ERR", "wrong number of arguments for 'set' command"),
        ),
        (
            Array.from_list(
                [
                    BulkString("set"),
                    BulkString("expiring"),
                    BulkString("value"),
                    BulkString("PXAT"),
                    BulkString("1702701491840"),
                ]
            ),
            SimpleString("OK"),
        ),
        # GET Tests
        (
            Array.from_list([BulkString("GET")]),
            Error("ERR", "wrong number of arguments for 'get' command"),
        ),
        (
            Array.from_list(
                [BulkString("get"), BulkString("key"), BulkString("value")]
            ),
            Error("ERR", "wrong number of arguments for 'get' command"),
        ),
        (
            Array.from_list([BulkString("get"), BulkString("key")]),
            BulkString("value"),
        ),
        (
            Array.from_list([BulkString("get"), BulkString("int_key_1")]),
            Integer(1),
        ),
        (
            Array.from_list([BulkString("get"), BulkString("non-existent")]),
            BulkString(None),
        ),
        (
            Array.from_list([BulkString("get"), BulkString("non-existent")]),
            BulkString(None),
        ),
        # EXISTS Tests
        (
            Array.from_list([BulkString("EXISTS")]),
            Error("ERR", "wrong number of arguments for 'exists' command"),
        ),
        (
            Array.from_list([BulkString("EXISTS"), BulkString("key")]),
            Integer(1),
        ),
        (
            Array.from_list([BulkString("exists"), BulkString("non-existent")]),
            Integer(0),
        ),
        (
            Array.from_list(
                [
                    BulkString("EXISTS"),
                    BulkString("key"),
                    BulkString("non-existent"),
                    BulkString("different_key"),
                ]
            ),
            Integer(2),
        ),
        # INCR Tests
        (
            Array.from_list([BulkString("INCR")]),
            Error("ERR", "wrong number of arguments for 'incr' command"),
        ),
        (
            Array.from_list(
                [BulkString("INCR"), BulkString("key"), BulkString("value")]
            ),
            Error("ERR", "wrong number of arguments for 'incr' command"),
        ),
        (
            Array.from_list([BulkString("INCR"), BulkString("key")]),
            Error("ERR", "value is not an integer or out of range"),
        ),
        (
            Array.from_list([BulkString("incr"), BulkString("int_key_2")]),
            Integer(1),
        ),
        (
            Array.from_list([BulkString("incr"), BulkString("int_key_1")]),
            Integer(2),
        ),
        # DECR Tests
        (
            Array.from_list([BulkString("DECR")]),
            Error("ERR", "wrong number of arguments for 'decr' command"),
        ),
        (
            Array.from_list(
                [BulkString("DECR"), BulkString("key"), BulkString("value")]
            ),
            Error("ERR", "wrong number of arguments for 'decr' command"),
        ),
        (
            Array.from_list([BulkString("decr"), BulkString("key")]),
            Error("ERR", "value is not an integer or out of range"),
        ),
        (
            Array.from_list([BulkString("DECR"), BulkString("int_key_2")]),
            Integer(0),
        ),
        (
            Array.from_list([BulkString("DECR"), BulkString("int_key_2")]),
            Integer(-1),
        ),
        (
            Array.from_list([BulkString("decr"), BulkString("int_key_3")]),
            Integer(-1),
        ),
        # LPUSH Tests
        (
            Array.from_list([BulkString("LPUSH")]),
            Error("ERR", "wrong number of arguments for 'lpush' command"),
        ),
        (
            Array.from_list([BulkString("LPUSH"), BulkString("key")]),
            Error("ERR", "wrong number of arguments for 'lpush' command"),
        ),
        (
            Array.from_list(
                [BulkString("lpush"), BulkString("list_1"), BulkString("value1")]
            ),
            Integer(1),
        ),
        (
            Array.from_list(
                [BulkString("lpush"), BulkString("list_1"), BulkString("value2")]
            ),
            Integer(2),
        ),
        (
            Array.from_list(
                [
                    BulkString("lpush"),
                    BulkString("list_1"),
                    BulkString("value3"),
                    BulkString("value4"),
                ]
            ),
            Integer(4),
        ),
        (
            Array.from_list([BulkString("GET"), BulkString("list_1")]),
            Error(
                "WRONGTYPE", "Operation against a key holding the wrong kind of value"
            ),
        ),
        # LRANGE Tests
        (
            Array.from_list([BulkString("LRANGE")]),
            Error("ERR", "wrong number of arguments for 'lrange' command"),
        ),
        (
            Array.from_list([BulkString("LRANGE"), BulkString("key")]),
            Error("ERR", "wrong number of arguments for 'lrange' command"),
        ),
        (
            Array.from_list([BulkString("LRANGE"), BulkString("key"), BulkString("0")]),
            Error("ERR", "wrong number of arguments for 'lrange' command"),
        ),
        (
            Array.from_list(
                [
                    BulkString("LRANGE"),
                    BulkString("key"),
                    BulkString("0"),
                    BulkString("-1"),
                    BulkString("0"),
                ]
            ),
            Error("ERR", "wrong number of arguments for 'lrange' command"),
        ),
        (
            Array.from_list(
                [
                    BulkString("LRANGE"),
                    BulkString("key"),
                    BulkString("0"),
                    BulkString("-1"),
                ]
            ),
            Array.from_list(
                [
                    BulkString("value1"),
                    BulkString("value2"),
                    BulkString("value3"),
                    BulkString("value4"),
                ]
            ),
        ),
        (
            Array.from_list(
                [
                    BulkString("LRANGE"),
                    BulkString("key"),
                    BulkString("1"),
                    BulkString("3"),
                ]
            ),
            Array.from_list(
                [BulkString("value2"), BulkString("value3"), BulkString("value4")]
            ),
        ),
        (
            Array.from_list(
                [
                    BulkString("LRANGE"),
                    BulkString("key"),
                    BulkString("-1"),
                    BulkString("4"),
                ]
            ),
            Array.from_list(
                [
                    BulkString("value1"),
                    BulkString("value2"),
                    BulkString("value3"),
                    BulkString("value4"),
                ]
            ),
        ),
        (
            Array.from_list(
                [
                    BulkString("LRANGE"),
                    BulkString("key"),
                    BulkString("0"),
                    BulkString("0"),
                ]
            ),
            Array.from_list([BulkString("value1")]),
        ),
        # DEL Tests
        (
            Array.from_list([BulkString("DEL")]),
            Error("ERR", "wrong number of arguments for 'del' command"),
        ),
        (
            Array.from_list([BulkString("DEL"), BulkString("key")]),
            Integer(1),
        ),
        (
            Array.from_list([BulkString("DEL"), BulkString("non-existent")]),
            Integer(0),
        ),
        (
            Array.from_list(
                [
                    BulkString("DEL"),
                    BulkString("different_key"),
                    BulkString("non-existent"),
                    BulkString("int_key_1"),
                ]
            ),
            Integer(2),
        ),
    ],
)
def test_handle_command(
    command: Array, expected: SimpleString | Error | BulkString
) -> None:
    result = handle_command(command, _DATA_STORE)
    assert result == expected


@pytest.mark.parametrize(
    "option, expiry",
    [("EX", "1"), ("PX", "1000"), ("EXAT", ""), ("PXAT", "")],
)
def test_expiry(option: str, expiry: str) -> None:
    if option == "EXAT":
        curr_time = datetime.now()
        expiry = str(time.mktime(curr_time.timetuple()) + 1)
    elif option == "PXAT":
        curr_time = datetime.now()
        expiry = str(time.mktime(curr_time.timetuple()) * 1000 + 1000)
    set_command = Array.from_list(
        [
            BulkString("set"),
            BulkString("key"),
            BulkString("value"),
            BulkString(option),
            BulkString(expiry),
        ]
    )
    result = handle_command(set_command, _DATA_STORE)
    assert result == SimpleString("OK")
    get_command = Array.from_list(
        [
            BulkString("get"),
            BulkString("key"),
        ]
    )
    result = handle_command(get_command, _DATA_STORE)
    assert result == BulkString("value")
    time.sleep(1)
    get_command = Array.from_list(
        [
            BulkString("get"),
            BulkString("key"),
        ]
    )
    result = handle_command(get_command, _DATA_STORE)
    assert result == BulkString(None)
