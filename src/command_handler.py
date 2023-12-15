from src.models.protocol.array import Array
from src.models.protocol.bulk_string import BulkString
from src.models.protocol.error import Error
from src.models.protocol.simple_string import SimpleString


def handle_command(command: Array) -> SimpleString | Error | BulkString | None:
    name, args = command[0], command[1:]
    match str(name).upper():
        case "PING":
            return handle_pong(args)
        case "ECHO":
            return handle_echo(args)
    return None


def handle_pong(
    args: list[SimpleString | BulkString],
) -> SimpleString | Error | BulkString:
    if len(args) == 0:
        return SimpleString("PONG")
    elif len(args) == 1:
        return args[0]
    else:
        return Error("ERR", "wrong number of arguments for 'ping' command")


def handle_echo(
    args: list[SimpleString | BulkString],
) -> SimpleString | Error | BulkString:
    if len(args) == 1:
        return args[0]
    else:
        return Error("ERR", "wrong number of arguments for 'echo' command")
