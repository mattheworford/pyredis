import pytest

from src.models.resp.data_types.array import Array
from src.models.resp.data_types.bulk_string import BulkString
from src.models.resp.resp_data_type import RespDataType
from src.models.resp.data_types.simple_string import SimpleString
from src.models.resp.data_types.error import Error
from src.models.resp.data_types.integer import Integer
from src.protocol_handler import extract_resp_data_and_size


@pytest.mark.parametrize(
    "payload, expected",
    [
        # Test cases for invalid payloads
        (b"PING\r\n", (None, 0)),
        # Test cases for Simple Strings
        (b"+PAR", (None, 0)),
        (b"+OK\r\n", (SimpleString("OK"), 5)),
        (b"+OK\r\nExtra data", (SimpleString("OK"), 5)),
        # Test cases for Errors
        (b"-Missing terminator", (None, 0)),
        (b"-Error message\r\n", (Error("", "Error message"), 16)),
        (
            b"-ERR unknown command 'asdf'\r\n",
            (Error("ERR", "unknown command 'asdf'"), 29),
        ),
        (b"-ERR\r\n", (Error("ERR", ""), 6)),
        (b"-Error message\r\nExtra data", (Error("", "Error message"), 16)),
        # Test cases for Integers
        (b":0", (None, 0)),
        (b":NaN\r\n", (Integer(None), 6)),
        (b":0\r\n", (Integer(0), 4)),
        (b":-1\r\n", (Integer(-1), 5)),
        (b":+123456789\r\n", (Integer(123456789), 13)),
        (b":1000\r\nextra", (Integer(1000), 7)),
        # Test cases for Bulk Strings
        (b"$1", (None, 0)),
        (b"$18\r\nMissing terminator", (None, 0)),
        (b"$NaN\r\nOK\r\n", (None, 0)),
        (b"$2\r\nOK\r\n", (BulkString("OK"), 8)),
        (b"$3\r\nToo long\r\n", (None, 0)),
        (b"$12\r\nToo short\r\n", (None, 0)),
        (b"$0\r\n\r\n", (BulkString(""), 6)),
        (b"$16\r\nLong bulk string\r\n", (BulkString("Long bulk string"), 23)),
        (b"$2\r\nOK\r\nextra", (BulkString("OK"), 8)),
        (b"$-1\r\n", (BulkString(None), 5)),
        # Test cases for Arrays
        (b"*1", (None, 0)),
        (b"*1\r\n+Missing terminator", (None, 0)),
        (b"*NaN\r\nOK\r\n", (None, 0)),
        (
            b"*2\r\n$5\r\nhello\r\n$5\r\nworld\r\n",
            (Array.from_list([BulkString("hello"), BulkString("world")]), 26),
        ),
        (
            b"*2\r\n:1\r\n$5\r\nhello\r\n",
            (Array.from_list([Integer(1), BulkString("hello")]), 19),
        ),
        (
            b"*2\r\n*1\r\n:1\r\n*1\r\n-Hello\r\n",
            (
                Array.from_list(
                    [
                        Array.from_list([Integer(1)]),
                        Array.from_list([Error("", "Hello")]),
                    ]
                ),
                24,
            ),
        ),
        (b"*1\r\n+Too\r\n+long\r\n", (Array.from_list([SimpleString("Too")]), 10)),
        (b"*12\r\n+Too short\r\n", (None, 0)),
        (b"*0\r\n", (Array.from_list([]), 4)),
        (b"*-1\r\n", (Array(None), 5)),
    ],
)
def test_extract_data_from_payload(
    payload: bytes,
    expected: tuple[RespDataType | None, int],
) -> None:
    actual = extract_resp_data_and_size(payload)
    assert actual == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        # Test cases for Simple Strings
        (SimpleString("OK"), b"+OK\r\n"),
        # Test cases for Errors
        (Error("", "Error"), b"-Error\r\n"),
        (Error("ERR", "Error"), b"-ERR Error\r\n"),
        # Test cases for Integers
        (Integer(100), b":100\r\n"),
        # Test cases for Bulk Strings
        (BulkString("This is a Bulk String"), b"$21\r\nThis is a Bulk String\r\n"),
        (BulkString(""), b"$0\r\n\r\n"),
        (BulkString(None), b"$-1\r\n"),
        # Test cases for Arrays
        (Array.from_list([]), b"*0\r\n"),
        (Array(None), b"*-1\r\n"),
        (
            Array.from_list(
                [SimpleString("String"), Integer(2), SimpleString("String2")]
            ),
            b"*3\r\n+String\r\n:2\r\n+String2\r\n",
        ),
    ],
)
def test_encode_data(data: RespDataType, expected: bytes) -> None:
    actual = data.encode()
    assert actual == expected
