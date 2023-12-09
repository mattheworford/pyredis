from src.models.protocol import SimpleString

CRLF = b"\r\n"


def extract_data_from_payload(payload):
    match chr(payload[0]):
        case '+':
            terminator = payload.find(CRLF)
            if terminator != -1:
                return SimpleString(payload[1:terminator].decode()), terminator + 2
    return None, 0
