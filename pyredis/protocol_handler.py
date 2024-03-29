import collections

from pyredis.models.resp.data_types.array import Array
from pyredis.models.resp.data_types.bulk_string import BulkString
from pyredis.models.resp.resp_data_type import RespDataType
from pyredis.models.resp.data_types.simple_string import SimpleString
from pyredis.models.resp.data_types.error import Error
from pyredis.models.resp.data_types.integer import Integer

TERMINATOR_SEQUENCE = b"\r\n"
TERMINATOR_SIZE = len(TERMINATOR_SEQUENCE)


def extract_resp_data_and_size(
    payload: bytes,
) -> tuple[RespDataType | None, int]:
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
                return _parse_integer_and_size(data, terminator_start)
            case "$":
                return _parse_bulk_string_and_size(data, remainder, terminator_start)
            case "*":
                return _parse_array_and_size(data, remainder, terminator_start)
        return None, 0


def _parse_integer_and_size(
    data: str, terminator_start: int
) -> tuple[Integer | None, int]:
    integer = Integer.from_string(data)
    return integer, terminator_start + TERMINATOR_SIZE


def _parse_bulk_string_and_size(
    data: str, remainder: bytes, terminator_start: int
) -> tuple[BulkString | None, int]:
    try:
        length = int(data)
    except ValueError:
        return None, 0
    if length == -1:
        return BulkString(None), 5
    first_terminator_end = terminator_start + TERMINATOR_SIZE
    second_terminator = remainder.find(TERMINATOR_SEQUENCE)
    if second_terminator != -1 and length == second_terminator:
        data = remainder[:second_terminator].decode()
        size = first_terminator_end + second_terminator + TERMINATOR_SIZE
        return BulkString(data), size
    else:
        return None, 0


def _parse_array_and_size(
    data: str, remainder: bytes, terminator_start: int
) -> tuple[Array | None, int]:
    try:
        number_of_elements = int(data)
    except ValueError:
        return None, 0
    if number_of_elements == -1:
        return Array(None), 5
    elements, size = collections.deque[RespDataType]([]), 0
    for _ in range(number_of_elements):
        curr_element, curr_size = extract_resp_data_and_size(remainder[size:])
        if curr_element is None:
            return None, 0
        elements.append(curr_element)
        size += curr_size
    return Array(elements), size + terminator_start + TERMINATOR_SIZE
