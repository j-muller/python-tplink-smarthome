from .device import TPLinkSmartDevice


class TPLinkSmartPlug(TPLinkSmartDevice):
    """An object to represent a physical smart plug.
    """

    def turn_on(self, id=None):
        """Turn on a smart plug.
        """
        cmd = {'system': {'set_relay_state': {'state': 1}}}
        if id is not None:
            cmd['context'] = {'child_ids': [id]}
        self.send(cmd)
        return self.recv()

    def turn_off(self, id=None):
        """Turn off a smart plug.
        """
        cmd = {'system': {'set_relay_state': {'state': 0}}}
        if id is not None:
            cmd['context'] = {'child_ids': [id]}
        self.send(cmd)
        return self.recv()

    def reboot(self):
        """Reboot a smart plug.
        """
        self.send({'system': {'reboot': {'delay': 1}}})

    def info(self):
        """Get information about a smart plug.
        """
        self.send({'system': {'get_sysinfo': {}}})
        return self.recv()
