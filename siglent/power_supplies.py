from .common import MessageResource


class SPD3303X(MessageResource):
    def __getitem__(self, channel: int):
        """Sets the current chanel"""
        assert channel == 1 or channel == 2, "Channel must be either 1 or 2"
        self._resource.query(f"INST CH{channel}")
        return self

    @property
    def current(self) -> float:
        """Gets the current of the currently selected channel"""
        return float(self._resource.query(f"MEAS:CURR?"))
