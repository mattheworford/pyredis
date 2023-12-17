from datetime import datetime, timedelta

from src.models.data_store import DataStore
from src.models.entry import Entry
from src.models.resp.data_types.array import Array
from src.models.resp.data_types.bulk_string import BulkString
from src.models.resp.data_types.error import Error
from src.models.resp.data_types.simple_string import SimpleString


def handle_command(
    command: Array, data_store: DataStore
) -> SimpleString | Error | BulkString | None:
    name, args = command[0], command[1:]
    match str(name).upper():
        case "PING":
            return _handle_pong(args)
        case "ECHO":
            return _handle_echo(args)
        case "SET":
            return _handle_set(args, data_store)
        case "GET":
            return _handle_get(args, data_store)
    return None


def _handle_pong(
    args: list[BulkString],
) -> SimpleString | BulkString | Error:
    if len(args) == 0:
        return SimpleString("PONG")
    elif len(args) == 1:
        return args[0]
    else:
        return Error.get_arg_num_error("ping")


def _handle_echo(
    args: list[BulkString],
) -> BulkString | Error:
    if len(args) == 1:
        return args[0]
    else:
        return Error.get_arg_num_error("echo")


def _handle_set(args: list[BulkString], data_store: DataStore) -> SimpleString | Error:
    if len(args) == 2:
        key, value = args[0].data, args[1].data
        if key is not None:
            try:
                data_store[key] = Entry(int(value), None)
            except ValueError:
                data_store[key] = Entry(value, None)
        return SimpleString("OK")
    if len(args) == 4:
        return _handle_set_with_expiry(args, data_store)
    else:
        return Error.get_arg_num_error("set")


def _handle_set_with_expiry(
    args: list[BulkString], data_store: DataStore
) -> SimpleString | Error:
    key, value, option, expiry_str = (
        args[0].data,
        args[1].data,
        args[2].data,
        args[3].data,
    )
    if key and option and expiry_str is not None:
        try:
            expiry = _get_expiry_datetime(option, float(expiry_str))
            if type(expiry) is datetime:
                try:
                    data_store[key] = Entry(int(value), None)
                except ValueError:
                    data_store[key] = Entry(value, None)
            elif type(expiry) is Error:
                return expiry
        except TypeError:
            return Error("ERR", "value is not an integer or out of range")
    return SimpleString("OK")


def _get_expiry_datetime(type_: str, expiry: float) -> datetime | Error:
    if type_ == "EX":
        return datetime.now() + timedelta(seconds=expiry)
    elif type_ == "PX":
        return datetime.now() + timedelta(milliseconds=expiry)
    elif type_ == "EXAT":
        return datetime.fromtimestamp(expiry)
    elif type_ == "PXAT":
        return datetime.fromtimestamp(expiry / 1000)

    return Error.get_arg_num_error("set")


def _handle_get(args: list[BulkString], data_store: DataStore) -> BulkString | Error:
    if len(args) == 1:
        key = args[0].data
        if key is None:
            return BulkString(None)
        try:
            entry = data_store[key]
            return BulkString(str(entry.value))
        except KeyError:
            return BulkString(None)
    else:
        return Error.get_arg_num_error("get")
