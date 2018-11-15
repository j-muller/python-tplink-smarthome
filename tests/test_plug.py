import pytest

from tplink_smarthome.plug import TPLinkSmartPlug


@pytest.mark.parametrize('method,send_param,send_call_count,recv_call_count', [
    ('turn_on', {'system': {'set_relay_state': {'state': 1}}}, 1, 1),
    ('turn_off', {'system': {'set_relay_state': {'state': 0}}}, 1, 1),
    ('reboot', {'system': {'reboot': {'delay': 1}}}, 1, 0),
    ('info', {'system': {'get_sysinfo': {}}}, 1, 1),
])
def test_smart_plug(mocker, method, send_param, send_call_count,
                    recv_call_count):
    device = TPLinkSmartPlug(host='127.0.0.1', connect=False)
    device.send = mocker.Mock()
    device.recv = mocker.Mock()

    # Call method
    getattr(device, method)()

    assert device.send.call_count == send_call_count
    assert device.recv.call_count == recv_call_count
    device.send.assert_called_with(send_param)
