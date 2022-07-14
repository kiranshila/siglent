from pyvisa import ResourceManager
from pyvisa.resources import MessageBasedResource


class MessageResource:
    def __init__(self, visa_address: str, rm: ResourceManager):
        res = rm.open_resource(visa_address)
        if isinstance(res, MessageBasedResource):
            self._resource = res
        else:
            raise TypeError("Selected resource isn't a Message-based resource")

    @property
    def identifier(self) -> str:
        """Returns a unique identifier of the deivce"""
        return self._resource.query("*IDN?")

    def reset(self):
        """
        This command presets the instrument to a factory defined condition that is appropriate for
        remote programming operation.
        """
        self._resource.write("*RST")

    def clear(self):
        """Clear the instrument status byte by emptying the error queue and clearing all event registers"""
        self._resource.write("*CLS")

    def block_until_complete(self):
        """Blocks the runtime until the instrument has finished all prior operations"""
        assert (
            self._resource.query("*OPC?").strip() == "1"
        ), "*OPC? returned something unexpected"
