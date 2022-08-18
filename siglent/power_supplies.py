"""Power suppliess.

# SPD3303X
WIP
"""

from .common import MessageResource


class SPD3303X(MessageResource):
    """The class to control a SPD3303X-Series power supply."""

    def __getitem__(self, channel: int):
        """Set the current chanel."""
        assert channel == 1 or channel == 2, "Channel must be either 1 or 2"
        self._resource.query(f"INST CH{channel}")
        return self

    @property
    def current(self) -> float:
        """Get the current of the currently selected channel."""
        return float(self._resource.query("MEAS:CURR?"))
