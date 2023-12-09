import pytest

from src.models.protocol import SimpleString
from src.protocol_handler import extract_data_from_payload


@pytest.mark.parametrize("payload, expected", [
    (b"+partial", (None, 0)),
    (b"+complete\r\n", (SimpleString("complete"), 11)),
    (b"+complete\r\nextra", (SimpleString("complete"), 11)),
])
def test_extract_simple_string_from_payload(payload, expected):
    actual = extract_data_from_payload(payload)
    assert actual == expected
