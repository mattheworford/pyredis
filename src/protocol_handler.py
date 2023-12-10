from src.models.protocol.array import Array
from src.models.protocol.bulk_string import BulkString
from src.models.protocol.simple_string import SimpleString
from src.models.protocol.error import Error

from src.models.protocol.integer import Integer

TERMINATOR_SEQUENCE = b"\r\n"


def extract_data_from_payload(payload):
    match chr(payload[0]):
        case '+':
            return extract_simple_string_from_payload(payload)
        case '-':
            return extract_error_from_payload(payload)
        case ':':
            return extract_integer_from_payload(payload)
        case '$':
            return extract_bulk_string_from_payload(payload)
        case '*':
            return extract_array_from_payload(payload)
    return None, 0


def extract_simple_string_from_payload(payload):
    terminator = payload.find(TERMINATOR_SEQUENCE)
    if terminator != -1:
        return SimpleString(payload[1:terminator].decode()), terminator + len(TERMINATOR_SEQUENCE)
    return None, 0


def extract_error_from_payload(payload):
    terminator = payload.find(TERMINATOR_SEQUENCE)
    if terminator != -1:
        return Error.from_string(payload[1:terminator].decode()), terminator + len(TERMINATOR_SEQUENCE)
    return None, 0


def extract_integer_from_payload(payload):
    terminator = payload.find(TERMINATOR_SEQUENCE)
    if terminator != -1:
        integer = Integer.from_string(payload[1:terminator].decode())
        if integer is not None:
            return integer, terminator + len(TERMINATOR_SEQUENCE)
    return None, 0


def extract_bulk_string_from_payload(payload):
    try:
        first_terminator_start = payload.find(TERMINATOR_SEQUENCE)
        if first_terminator_start != -1:
            length = int(payload[1:first_terminator_start].decode())
            if length == -1:
                return None, 5
            first_terminator_end = first_terminator_start + len(TERMINATOR_SEQUENCE)
            second_terminator = payload[first_terminator_end:].find(TERMINATOR_SEQUENCE)
            if second_terminator != -1 and length == second_terminator:
                data = payload[first_terminator_end:first_terminator_end + second_terminator].decode()
                size = first_terminator_end + second_terminator + len(TERMINATOR_SEQUENCE)
                return BulkString(data), size
    except ValueError:
        return None, 0
    return None, 0


def extract_array_from_payload(payload):
    try:
        terminator = payload.find(TERMINATOR_SEQUENCE)
        if terminator != -1:
            number_of_elements = int(payload[1:terminator].decode())
            if number_of_elements == -1:
                return None, 5
            elements, size = [], terminator + len(TERMINATOR_SEQUENCE)
            for _ in range(number_of_elements):
                if size >= len(payload)-1:
                    return None, 0
                curr_element, curr_size = extract_data_from_payload(payload[size:])
                if curr_size == 0:
                    return None, 0
                elements.append(curr_element)
                size += curr_size
            return Array(elements), size
    except ValueError:
        return None, 0
    return None, 0
