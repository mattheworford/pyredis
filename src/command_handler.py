import builtins
import collections
from datetime import datetime, timedelta
from typing import Any

from src.models.data_store import DataStore
from src.models.entry import Entry
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
from src.models.resp.resp_data_type import RespDataType


def handle_command(command: Array, data_store: DataStore) -> RespDataType:
    name, args = command.popleft(), command
    match str(name).upper():
        case "PING":
            return _handle_pong(args)
        case "ECHO":
            return _handle_echo(args)
        case "SET":
            return _handle_set(args, data_store)
        case "GET":
            return _handle_get(args, data_store)
        case "EXISTS":
            return _handle_exists(args, data_store)
        case "INCR":
            return _handle_incr(args, data_store)
        case "DECR":
            return _handle_decr(args, data_store)
        case "LPUSH":
            return _handle_lpush(args, data_store)
        case "RPUSH":
            return _handle_rpush(args, data_store)
        case "LRANGE":
            return _handle_lrange(args, data_store)
        case "DEL":
            return _handle_del(args, data_store)
    return Error("ERR", f"unknown command '{name}', with args beginning with")


def _handle_pong(
    args: Array,
) -> RespDataType:
    if len(args) == 0:
        return SimpleString("PONG")
    elif len(args) == 1:
        return args.popleft()
    else:
        return NumberOfArgumentsError("ping")


def _handle_echo(
    args: Array,
) -> RespDataType:
    if len(args) == 1:
        return args.popleft()
    else:
        return NumberOfArgumentsError("echo")


def _handle_set(args: Array, data_store: DataStore) -> SimpleString | Error:
    if len(args) == 2 or len(args) == 4:
        key, value, expiry = str(args.popleft()), str(args.popleft()), _get_expiry(args)
        if isinstance(expiry, Error):
            return expiry
        try:
            data_store[key] = Entry(int(value), expiry)
        except ValueError:
            data_store[key] = Entry(value, expiry)
        return SimpleString("OK")
    else:
        return NumberOfArgumentsError("set")


def _get_expiry(args: Array) -> datetime | None | Error:
    if len(args) == 0:
        return None
    try:
        option, expiry = (
            str(args.popleft()),
            float(str(args.popleft())),
        )
    except TypeError:
        return NonIntOrOutOfRangeError()
    match option.upper():
        case "EX":
            return datetime.now() + timedelta(seconds=expiry)
        case "PX":
            return datetime.now() + timedelta(milliseconds=expiry)
        case "EXAT":
            return datetime.fromtimestamp(expiry)
        case "PXAT":
            return datetime.fromtimestamp(expiry / 1000)
    return NumberOfArgumentsError("set")


def _handle_get(args: Array, data_store: DataStore) -> RespDataType:
    if len(args) == 1:
        key = str(args.popleft())
        if key not in data_store:
            return BulkString(None)
        value = data_store[key].value
        if isinstance(value, int):
            return Integer(value)
        elif isinstance(value, str):
            return BulkString(value)
        else:
            return WrongValueTypeError()
    else:
        return NumberOfArgumentsError("get")


def _handle_exists(args: Array, data_store: DataStore) -> Integer | Error:
    if len(args) > 0:
        num_exist = sum(1 for arg in args if (str(arg) in data_store))
        return Integer(num_exist)
    else:
        return NumberOfArgumentsError("exists")


def _handle_incr(args: Array, data_store: DataStore) -> Integer | Error:
    if len(args) == 1:
        key = str(args.popleft())
        entry = data_store.get(key, Entry(0, None))
        if type(entry.value) is int:
            entry.value += 1
            data_store[key] = entry
            return Integer(entry.value)
        else:
            return NonIntOrOutOfRangeError()
    return NumberOfArgumentsError("incr")


def _handle_decr(args: Array, data_store: DataStore) -> Integer | Error:
    if len(args) == 1:
        key = str(args.popleft())
        entry = data_store.get(key, Entry(0, None))
        if type(entry.value) is int:
            entry.value -= 1
            data_store[key] = entry
            return Integer(entry.value)
        else:
            return NonIntOrOutOfRangeError()
    else:
        return NumberOfArgumentsError("decr")


def _handle_lpush(args: Array, data_store: DataStore) -> Integer | Error:
    if len(args) > 1:
        key = str(args.popleft())
        entry = data_store.get(key, Entry(collections.deque([]), None))
        if not isinstance(entry.value, collections.deque):
            return WrongValueTypeError()
        for element in args:
            entry.value.appendleft(element.underlying())
        data_store[key] = entry
        return Integer(len(entry.value))
    return NumberOfArgumentsError("lpush")


def _handle_rpush(args: Array, data_store: DataStore) -> Integer | Error:
    if len(args) > 1:
        key = str(args.popleft())
        entry = data_store.get(key, Entry(collections.deque([]), None))
        if not isinstance(entry.value, collections.deque):
            return WrongValueTypeError()
        for element in args:
            entry.value.append(element.underlying())
        data_store[key] = entry
        return Integer(len(entry.value))
    return NumberOfArgumentsError("rpush")


def _handle_lrange(args: Array, data_store: DataStore) -> Array | Error:
    if len(args) == 3:
        try:
            key, start, stop = (
                str(args.popleft()),
                int(str(args.popleft())),
                int(str(args.popleft())),
            )
        except ValueError:
            return NonIntOrOutOfRangeError()
        entry = data_store.get(key, Entry(collections.deque([]), None))
        if not isinstance(entry.value, collections.deque):
            return WrongValueTypeError()
        stop = stop if 0 <= stop < len(entry.value) else (len(entry.value) - 1)
        slice_: collections.deque[Any] = collections.deque([])
        for i, value in enumerate(entry.value):
            if i > stop:
                break
            if start <= i:
                slice_.append(value)
        return Array.from_any_deque(slice_)
    return NumberOfArgumentsError("lrange")


def _handle_del(args: Array, data_store: DataStore) -> Integer | Error:
    if len(args) > 0:
        num_deleted = 0
        for arg in args:
            key = str(arg)
            if key in data_store:
                del data_store[key]
                num_deleted += 1
        return Integer(num_deleted)
    else:
        return NumberOfArgumentsError("del")
