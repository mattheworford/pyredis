from datetime import datetime, timedelta

from src.models.data_store import DataStore
from src.models.entry import Entry
from src.models.resp.data_types.array import Array
from src.models.resp.data_types.bulk_string import BulkString
from src.models.resp.data_types.error import Error
from src.models.resp.data_types.integer import Integer
from src.models.resp.data_types.simple_string import SimpleString
from src.models.resp.resp_data_type import RespDataType


def handle_command(command: Array, data_store: DataStore) -> RespDataType:
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
        case "EXISTS":
            return _handle_exists(args, data_store)
        case "DEL":
            return _handle_del(args, data_store)
    return Error("ERR", f"unknown command '{name}', with args beginning with")


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
                data_store[key] = Entry(value, expiry)
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


def _handle_get(args: list[BulkString], data_store: DataStore) -> BulkString | Error:
    if len(args) == 1:
        key = args[0].data
        if key is None:
            return BulkString(None)
        try:
            entry = data_store[key]
            return BulkString(entry.value)
        except KeyError:
            return BulkString(None)
    else:
        return Error.get_arg_num_error("get")


def _handle_exists(args: list[BulkString], data_store: DataStore) -> Integer | Error:
    if len(args) > 0:
        num_exist = 0
        for arg in args:
            key = arg.data
            if key is None:
                continue
            try:
                if data_store[key]:
                    num_exist += 1
            except KeyError:
                continue
        return Integer(num_exist)
    else:
        return Error.get_arg_num_error("exists")


def _handle_del(args: list[BulkString], data_store: DataStore) -> Integer | Error:
    if len(args) > 0:
        num_deleted = 0
        for arg in args:
            key = arg.data
            if key is None:
                continue
            try:
                if data_store[key]:
                    del data_store[key]
                    num_deleted += 1
            except KeyError:
                continue
        return Integer(num_deleted)
    else:
        return Error.get_arg_num_error("del")
