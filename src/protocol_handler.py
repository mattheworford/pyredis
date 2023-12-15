from src.models.protocol.array import Array
from src.models.protocol.bulk_string import BulkString
from src.models.protocol.simple_string import SimpleString
from src.models.protocol.error import Error
from src.models.protocol.integer import Integer

TERMINATOR_SEQUENCE = b"\r\n"
TERMINATOR_SIZE = len(TERMINATOR_SEQUENCE)


def extract_data_from_payload(
    payload: bytes,
) -> tuple[SimpleString | Error | Integer | BulkString | Array | None, int]:
    terminator_start = payload.find(TERMINATOR_SEQUENCE)
    if terminator_start == -1:
        return None, 0
    else:
        data = payload[1:terminator_start].decode()
        remainder = payload[terminator_start + TERMINATOR_SIZE :]
        match chr(payload[0]):
            case "+":
                return SimpleString(data), terminator_start + TERMINATOR_SIZE
            case "-":
                return Error.from_string(data), terminator_start + TERMINATOR_SIZE
            case ":":
                return parse_integer_and_size(data, terminator_start)
            case "$":
                return parse_bulk_string_and_size(data, remainder, terminator_start)
            case "*":
                return parse_array_and_size(data, remainder, terminator_start)
        return None, 0


def parse_integer_and_size(
    data: str, terminator_start: int
) -> tuple[Integer | None, int]:
    integer = Integer.from_string(data)
    if integer is not None:
        return integer, terminator_start + TERMINATOR_SIZE
    return None, 0


def parse_bulk_string_and_size(
    data: str, remainder: bytes, terminator_start: int
) -> tuple[BulkString | None, int]:
    try:
        length = int(data)
        if length == -1:
            return BulkString(None), 5
        first_terminator_end = terminator_start + TERMINATOR_SIZE
        second_terminator = remainder.find(TERMINATOR_SEQUENCE)
        if second_terminator != -1 and length == second_terminator:
            data = remainder[:second_terminator].decode()
            size = first_terminator_end + second_terminator + TERMINATOR_SIZE
            return BulkString(data), size
    except ValueError:
        return None, 0
    return None, 0


def parse_array_and_size(
    data: str, remainder: bytes, terminator_start: int
) -> tuple[Array | None, int]:
    try:
        number_of_elements = int(data)
        if number_of_elements == -1:
            return Array(None), 5
        elements, size = [], 0
        for _ in range(number_of_elements):
            if size >= len(remainder) - 1:
                return None, 0
            curr_element, curr_size = extract_data_from_payload(remainder[size:])
            if curr_size == 0:
                return None, 0
            elements.append(curr_element)
            size += curr_size
        return Array(elements), size + terminator_start + TERMINATOR_SIZE
    except ValueError:
        return None, 0


def encode_data(data: SimpleString | Error | Integer | BulkString | Array) -> bytes:
    return data.resp_encode()
