import builtins
import collections
from datetime import datetime, timedelta
from typing import Any

from src.models.data_store import DataStore
from src.models.entry import Entry
from src.models.resp.data_types.array import Array
from src.models.resp.data_types.bulk_string import BulkString
from src.models.resp.data_types.error import Error
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
        return Error.get_arg_num_error("ping")


def _handle_echo(
    args: Array,
) -> RespDataType:
    if len(args) == 1:
        return args.popleft()
    else:
        return Error.get_arg_num_error("echo")


def _handle_set(args: Array, data_store: DataStore) -> SimpleString | Error:
    if len(args) == 2:
        key, value = args.popleft(), args.popleft()
        try:
            data_store[str(key)] = Entry(int(str(value)), None)
        except ValueError:
            data_store[str(key)] = Entry(value, None)
        return SimpleString("OK")
    if len(args) == 4:
        return _handle_set_with_expiry(args, data_store)
    else:
        return Error.get_arg_num_error("set")


def _handle_set_with_expiry(args: Array, data_store: DataStore) -> SimpleString | Error:
    key, value, option, expiry_str = (
        args.popleft(),
        args.popleft(),
        args.popleft(),
        args.popleft(),
    )
    try:
        expiry = _get_expiry_datetime(str(option), float(str(expiry_str)))
        if type(expiry) is datetime:
            try:
                data_store[str(key)] = Entry(int(str(value)), expiry)
            except ValueError:
                data_store[str(key)] = Entry(value, expiry)
        elif type(expiry) is Error:
            return expiry
    except TypeError:
        return Error("ERR", "value is not an integer or out of range")
    return SimpleString("OK")


def _get_expiry_datetime(type_: str, expiry: float) -> datetime | Error:
    match type_.upper():
        case "EX":
            return datetime.now() + timedelta(seconds=expiry)
        case "PX":
            return datetime.now() + timedelta(milliseconds=expiry)
        case "EXAT":
            return datetime.fromtimestamp(expiry)
        case "PXAT":
            return datetime.fromtimestamp(expiry / 1000)

    return Error.get_arg_num_error("set")


def _handle_get(args: Array, data_store: DataStore) -> RespDataType:
    if len(args) == 1:
        key = args.popleft()
        try:
            entry = data_store[str(key)]
            match type(entry.value):
                case builtins.int:
                    return Integer(entry.value)
                case collections.deque:
                    return Error(
                        "WRONGTYPE",
                        "Operation against a key holding the wrong kind of value",
                    )
            return BulkString(str(entry.value))
        except KeyError:
            return BulkString(None)
    else:
        return Error.get_arg_num_error("get")


def _handle_exists(args: Array, data_store: DataStore) -> Integer | Error:
    if len(args) > 0:
        num_exist = 0
        while len(args) > 0:
            key = args.popleft()
            try:
                if data_store[str(key)]:
                    num_exist += 1
            except KeyError:
                continue
        return Integer(num_exist)
    else:
        return Error.get_arg_num_error("exists")


def _handle_incr(args: Array, data_store: DataStore) -> Integer | Error:
    if len(args) == 1:
        key = args.popleft()
        try:
            entry = data_store[str(key)]
            if type(entry.value) is int:
                entry.value += 1
                data_store[str(key)] = entry
                return Integer(entry.value)
            else:
                return Error("ERR", "value is not an integer or out of range")
        except KeyError:
            data_store[str(key)] = Entry(1, None)
            return Integer(1)
    return Error.get_arg_num_error("incr")


def _handle_decr(args: Array, data_store: DataStore) -> Integer | Error:
    if len(args) == 1:
        key = args.popleft()
        try:
            entry = data_store[str(key)]
            if type(entry.value) is int:
                entry.value -= 1
                data_store[str(key)] = entry
                return Integer(entry.value)
            else:
                return Error("ERR", "value is not an integer or out of range")
        except KeyError:
            data_store[str(key)] = Entry(-1, None)
            return Integer(-1)
    return Error.get_arg_num_error("decr")


def _handle_lpush(args: Array, data_store: DataStore) -> Integer | Error:
    if len(args) > 1:
        key = args.popleft()
        entry = Entry(collections.deque([]), None)
        try:
            if type(data_store[str(key)].value) is collections.deque:
                entry = data_store[str(key)]
            else:
                return Error(
                    "WRONGTYPE",
                    "Operation against a key holding the wrong kind of value",
                )
        except KeyError:
            pass
        while len(args) > 0:
            element = args.popleft()
            entry.value.appendleft(element.underlying())
        data_store[str(key)] = entry
        return Integer(len(entry.value))
    return Error.get_arg_num_error("lpush")


def _handle_rpush(args: Array, data_store: DataStore) -> Integer | Error:
    if len(args) > 1:
        key = args.popleft()
        entry = Entry(collections.deque([]), None)
        try:
            if type(data_store[str(key)].value) is collections.deque:
                entry = data_store[str(key)]
            else:
                return Error(
                    "WRONGTYPE",
                    "Operation against a key holding the wrong kind of value",
                )
        except KeyError:
            pass
        while len(args) > 0:
            element = args.popleft()
            entry.value.append(element.underlying())
        data_store[str(key)] = entry
        return Integer(len(entry.value))
    return Error.get_arg_num_error("rpush")


def _handle_lrange(args: Array, data_store: DataStore) -> Array | Error:
    if len(args) == 3:
        try:
            key, start, stop = (
                args.popleft(),
                int(str(args.popleft())),
                int(str(args.popleft())),
            )
        except ValueError:
            return Error("ERR", "value is not an integer or out of range")
        entry = Entry(collections.deque([]), None)
        try:
            if type(data_store[str(key)].value) is collections.deque:
                entry = data_store[str(key)]
            else:
                return Error(
                    "WRONGTYPE",
                    "Operation against a key holding the wrong kind of value",
                )
        except KeyError:
            pass
        start, stop = start if 0 <= start < len(
            entry.value
        ) else 0, stop if 0 <= stop < len(entry.value) else (len(entry.value) - 1)
        slice_: collections.deque[Any] = collections.deque([])
        for i, value in enumerate(entry.value):
            if i > stop:
                break
            if start <= i <= stop:
                slice_.append(value)
        return Array.from_any_deque(slice_)
    return Error.get_arg_num_error("lrange")


def _handle_del(args: Array, data_store: DataStore) -> Integer | Error:
    if len(args) > 0:
        num_deleted = 0
        while len(args) > 0:
            key = args.popleft()
            if key is None:
                continue
            try:
                if data_store[str(key)]:
                    del data_store[str(key)]
                    num_deleted += 1
            except KeyError:
                continue
        return Integer(num_deleted)
    else:
        return Error.get_arg_num_error("del")
