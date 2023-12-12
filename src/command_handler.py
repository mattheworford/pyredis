from src.models.protocol.error import Error, WrongNumberOfArgumentsError
from src.models.protocol.simple_string import SimpleString


def handle_command(command):
    type, args = command[0], command[1:]
    match str(type).upper():
        case "PING":
            return handle_pong(args)
        case "ECHO":
            return handle_echo(args)
    return None, 0


def handle_pong(args):
    if len(args) == 0:
        return SimpleString("PONG")
    elif len(args) == 1:
        return args[0]
    else:
        return WrongNumberOfArgumentsError("ping")


def handle_echo(args):
    if len(args) == 1:
        return args[0]
    else:
        return WrongNumberOfArgumentsError("echo")
