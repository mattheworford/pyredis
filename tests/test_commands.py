import time
from datetime import datetime

import pytest

from src.command_handler import handle_command
from src.models.append_only_persister import AppendOnlyPersister
from src.models.data_store import DataStore
from src.models.resp.data_types.array import Array
from src.models.resp.data_types.bulk_string import BulkString
from src.models.resp.data_types.error import (
    Error,
    NumberOfArgumentsError,
    WrongValueTypeError,
    NonIntOrOutOfRangeError,
)
from src.models.resp.data_types.integer import Integer
from src.models.resp.data_types.simple_string import SimpleString

_DATA_STORE = DataStore()
_PERSISTER = AppendOnlyPersister("test.aof")


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
            NumberOfArgumentsError("echo"),
        ),
        (
            Array.from_list([BulkString("ECHO"), BulkString("Hello")]),
            BulkString("Hello"),
        ),
        (
            Array.from_list(
                [BulkString("echo"), BulkString("Hello"), BulkString("World")]
            ),
            NumberOfArgumentsError("echo"),
        ),
        # SET Tests
        (
            Array.from_list([BulkString("SET")]),
            NumberOfArgumentsError("set"),
        ),
        (
            Array.from_list([BulkString("set"), BulkString("key")]),
            NumberOfArgumentsError("set"),
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
            NumberOfArgumentsError("set"),
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
            NumberOfArgumentsError("set"),
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
            NumberOfArgumentsError("set"),
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
            NumberOfArgumentsError("set"),
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
            NumberOfArgumentsError("get"),
        ),
        (
            Array.from_list(
                [BulkString("get"), BulkString("key"), BulkString("value")]
            ),
            NumberOfArgumentsError("get"),
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
            NumberOfArgumentsError("exists"),
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
            NumberOfArgumentsError("incr"),
        ),
        (
            Array.from_list(
                [BulkString("INCR"), BulkString("key"), BulkString("value")]
            ),
            NumberOfArgumentsError("incr"),
        ),
        (
            Array.from_list([BulkString("INCR"), BulkString("key")]),
            NonIntOrOutOfRangeError(),
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
            NumberOfArgumentsError("decr"),
        ),
        (
            Array.from_list(
                [BulkString("DECR"), BulkString("key"), BulkString("value")]
            ),
            NumberOfArgumentsError("decr"),
        ),
        (
            Array.from_list([BulkString("decr"), BulkString("key")]),
            NonIntOrOutOfRangeError(),
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
            NumberOfArgumentsError("lpush"),
        ),
        (
            Array.from_list([BulkString("LPUSH"), BulkString("key")]),
            NumberOfArgumentsError("lpush"),
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
            WrongValueTypeError(),
        ),
        # RPUSH Tests
        (
            Array.from_list([BulkString("RPUSH")]),
            NumberOfArgumentsError("rpush"),
        ),
        (
            Array.from_list([BulkString("rpush"), BulkString("key")]),
            NumberOfArgumentsError("rpush"),
        ),
        (
            Array.from_list(
                [BulkString("rpush"), BulkString("list_2"), BulkString("value1")]
            ),
            Integer(1),
        ),
        (
            Array.from_list(
                [BulkString("RPUSH"), BulkString("list_2"), BulkString("value2")]
            ),
            Integer(2),
        ),
        (
            Array.from_list(
                [
                    BulkString("RPUSH"),
                    BulkString("list_2"),
                    BulkString("value3"),
                    BulkString("value4"),
                ]
            ),
            Integer(4),
        ),
        # LRANGE Tests
        (
            Array.from_list([BulkString("LRANGE")]),
            NumberOfArgumentsError("lrange"),
        ),
        (
            Array.from_list([BulkString("LRANGE"), BulkString("key")]),
            NumberOfArgumentsError("lrange"),
        ),
        (
            Array.from_list([BulkString("LRANGE"), BulkString("key"), BulkString("0")]),
            NumberOfArgumentsError("lrange"),
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
            NumberOfArgumentsError("lrange"),
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
            WrongValueTypeError(),
        ),
        (
            Array.from_list(
                [
                    BulkString("LRANGE"),
                    BulkString("list_1"),
                    BulkString("0"),
                    BulkString("-1"),
                ]
            ),
            Array.from_list(
                [
                    BulkString("value4"),
                    BulkString("value3"),
                    BulkString("value2"),
                    BulkString("value1"),
                ]
            ),
        ),
        (
            Array.from_list(
                [
                    BulkString("LRANGE"),
                    BulkString("list_2"),
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
                    BulkString("list_1"),
                    BulkString("1"),
                    BulkString("3"),
                ]
            ),
            Array.from_list(
                [BulkString("value3"), BulkString("value2"), BulkString("value1")]
            ),
        ),
        (
            Array.from_list(
                [
                    BulkString("LRANGE"),
                    BulkString("list_1"),
                    BulkString("-1"),
                    BulkString("4"),
                ]
            ),
            Array.from_list(
                [
                    BulkString("value4"),
                    BulkString("value3"),
                    BulkString("value2"),
                    BulkString("value1"),
                ]
            ),
        ),
        (
            Array.from_list(
                [
                    BulkString("LRANGE"),
                    BulkString("list_1"),
                    BulkString("0"),
                    BulkString("0"),
                ]
            ),
            Array.from_list([BulkString("value4")]),
        ),
        (
            Array.from_list(
                [
                    BulkString("LRANGE"),
                    BulkString("list_1"),
                    BulkString("3"),
                    BulkString("0"),
                ]
            ),
            Array.from_list([]),
        ),
        # DEL Tests
        (
            Array.from_list([BulkString("DEL")]),
            NumberOfArgumentsError("del"),
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
    result = handle_command(command, _DATA_STORE, _PERSISTER)
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
    result = handle_command(set_command, _DATA_STORE, _PERSISTER)
    assert result == SimpleString("OK")
    get_command = Array.from_list(
        [
            BulkString("get"),
            BulkString("key"),
        ]
    )
    result = handle_command(get_command, _DATA_STORE, _PERSISTER)
    assert result == BulkString("value")
    time.sleep(1)
    get_command = Array.from_list(
        [
            BulkString("get"),
            BulkString("key"),
        ]
    )
    result = handle_command(get_command, _DATA_STORE, _PERSISTER)
    assert result == BulkString(None)
