from src.models.data_store import DataStore
from src.models.protocol.array import Array
from src.models.protocol.bulk_string import BulkString
from src.models.protocol.error import Error
from src.models.protocol.simple_string import SimpleString


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
    args: list[SimpleString | BulkString],
) -> SimpleString | Error | BulkString:
    if len(args) == 0:
        return SimpleString("PONG")
    elif len(args) == 1:
        return args[0]
    else:
        return Error.wrong_arg_num("ping")


def _handle_echo(
    args: list[SimpleString | BulkString],
) -> SimpleString | Error | BulkString:
    if len(args) == 1:
        return args[0]
    else:
        return Error.wrong_arg_num("echo")


def _handle_set(
    args: list[SimpleString | BulkString], data_store: DataStore
) -> SimpleString | Error | BulkString:
    if len(args) == 2:
        key, value = args[0].data, args[1].data
        if key is not None:
            data_store[key] = value
        return SimpleString("OK")
    else:
        return Error.wrong_arg_num("set")


def _handle_get(
    args: list[SimpleString | BulkString], data_store: DataStore
) -> SimpleString | Error | BulkString:
    if len(args) == 1:
        key = args[0].data
        if key is None:
            return SimpleString("")
        try:
            return BulkString(data_store[key])
        except KeyError:
            return SimpleString("")
    else:
        return Error.wrong_arg_num("get")
