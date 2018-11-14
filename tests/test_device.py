# pylint: disable=redefined-outer-name
import pytest

from tplink_smarthome.device import TPLinkSmartDevice


# pylint: disable=protected-access
@pytest.fixture
def device(mocker):
    device = TPLinkSmartDevice(host='127.0.0.1', connect=False)
    device._TPLinkSmartDevice__socket = mocker.Mock()
    return device


def test_sanity(mocker, device):
    assert device.host == '127.0.0.1'
    assert device.port == TPLinkSmartDevice.DEFAULT_PORT
    assert isinstance(device.socket, mocker.Mock)


def test_send(device):
    expected_argument = [0x0, 0x0, 0x0, 0xe, 0xd0, 0xf2, 0x94, 0xfb, 0x94,
                         0xb6, 0x8c, 0xac, 0x8e, 0xec, 0x8d, 0xff, 0xdd,
                         0xa0]

    device.send({'foo': 'bar'})
    assert device.socket.send.call_count == 1
    device.socket.send.assert_called_with(bytes(expected_argument))

    expected_argument = [0x0, 0x0, 0x0, 0xe, 0xd0, 0xf7, 0x91, 0xfe, 0x91,
                         0xb6, 0x8c, 0xac, 0x8b, 0xe9, 0x88, 0xf2, 0xd5, 0xa8]
    device.send("{'foo': 'baz'}")
    assert device.socket.send.call_count == 2
    device.socket.send.assert_called_with(bytes(expected_argument))


def test_close(device):
    device.close()
    assert device.socket is None


def test_recv(device):
    message = [0x0, 0x0, 0x0, 0x2d, 0xd0, 0xf2, 0x81, 0xf8, 0x8b, 0xff,
               0x9a, 0xf7, 0xd5, 0xef, 0x94, 0xb6, 0xc5, 0xa0, 0xd4, 0x8b,
               0xf9, 0x9c, 0xf0, 0x91, 0xe8, 0xb7, 0xc4, 0xb0, 0xd1, 0xa5,
               0xc0, 0xe2, 0xd8, 0xa3, 0x81, 0xe4, 0x96, 0xe4, 0xbb, 0xd8,
               0xb7, 0xd3, 0xb6, 0x94, 0xae, 0x9e, 0xe3, 0x9e, 0xe3]
    device.socket.recv.return_value = bytes(message)

    expected_result = {'system': {'set_relay_state': {'err_code': 0}}}
    result = device.recv()
    assert result == expected_result
