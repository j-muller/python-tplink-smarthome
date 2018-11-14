import struct

# XOR starting key
_KEY = 171


def encrypt(message):
    """Encrypt a message in TP-Link protocol.

    :param message: `string` message to encrypt.
    """
    result = bytearray(struct.pack('>I', len(message)))
    key = _KEY

    for byte in message.encode():
        temp = key ^ byte
        key = temp
        result.append(temp)

    return result


def decrypt(message):
    """Decrypt a message in TP-Link protocol.

    :param message: `string` message to decrypt.
    """
    key = _KEY
    result = bytes()

    for byte in message:
        temp = key ^ byte
        key = byte
        result += struct.pack('>b', temp)

    return result.decode()
