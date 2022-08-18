"""Commom utilities for working with all siglent GPIB devices."""

from pyvisa import ResourceManager
from pyvisa.resources import MessageBasedResource


class MessageResource:
    """Base class for all message-based siglent gpib resources."""

    def __init__(self, visa_address: str, rm: ResourceManager):
        res = rm.open_resource(visa_address)
        if isinstance(res, MessageBasedResource):
            self._resource = res
        else:
            raise TypeError("Selected resource isn't a Message-based resource")

    @property
    def identifier(self) -> str:
        """Get the unique identifier of the deivce."""
        return self._resource.query("*IDN?")

    def reset(self):
        """Reset the instrument to a factory defined condition."""
        self._resource.write("*RST")

    def clear(self):
        """Clear the instrument status byte."""
        self._resource.write("*CLS")

    def block_until_complete(self):
        """Block the runtime until the instrument has finished all prior operations."""
        assert (
            self._resource.query("*OPC?").strip() == "1"
        ), "*OPC? returned something unexpected"
