from src.models.data_store import DataStore
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
            data_store[key] = value
        return SimpleString("OK")
    else:
        return Error.get_arg_num_error("set")


def _handle_get(args: list[BulkString], data_store: DataStore) -> BulkString | Error:
    if len(args) == 1:
        key = args[0].data
        if key is None:
            return BulkString(None)
        try:
            return BulkString(data_store[key])
        except KeyError:
            return BulkString(None)
    else:
        return Error.get_arg_num_error("get")
