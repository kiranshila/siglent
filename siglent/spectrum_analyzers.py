from enum import Enum
import numpy as np
from common import MessageResource


class Bandwidth(Enum):
    """The discrete bandwidth values for Resolution and Video Bandwidth"""

    HZ_1 = 1
    HZ_3 = 3
    HZ_10 = 10
    HZ_30 = 30
    HZ_100 = 100
    HZ_300 = 30
    KHZ_1 = 1e3
    KHZ_3 = 3e3
    KHZ_10 = 10e3
    KHZ_30 = 30e3
    KHZ_100 = 100e3
    KHZ_300 = 300e3
    MHZ_1 = 1e6


class AverageType(Enum):
    LOG_POWER = "LOGP"
    POWER = "POW"
    VOLTAGE = "VOLT"


class SSA3000X(MessageResource):
    @property
    def ref_level(self) -> float:
        """Gets the current reference level in dBm"""
        return float(self._resource.query(f":DISP:WIND:TRAC:Y:RLEV?"))

    # ----- Display -----

    @ref_level.setter
    def ref_level(self, level_dbm: float):
        """Sets the reference level to the specified value in dBm"""
        assert -100 <= level_dbm <= 30, "Level must be between -100 and 30 dBm"
        self._resource.write(f":DISP:WIND:TRAC:Y:RLEV {level_dbm} DBM")

    # ----- Frequency -----

    @property
    def span(self) -> float:
        """Gets the current span in Hz"""
        return float(self._resource.query(":FREQ:SPAN?"))

    @span.setter
    def span(self, freq_hz: float):
        """Sets the span in Hz"""
        assert (100 <= freq_hz <= 3.2e9) or (
            freq_hz == 0
        ), "Span must be between 100 Hz and 3.2 GHz or 0"
        self._resource.write(f":FREQ:SPAN {freq_hz} Hz")

    @property
    def freq_center(self) -> float:
        """Gets the center frequency in Hz"""
        return float(self._resource.query(":FREQ:CENT?"))

    @freq_center.setter
    def freq_center(self, freq_hz: float):
        """Sets the center frequency in Hz"""
        assert 0 <= freq_hz <= 3.2e9, "Center frequency must be between 0 and 3.2 GHz"
        self._resource.write(f":FREQ:CENT {freq_hz} Hz")

    @property
    def freq_start(self) -> float:
        """Gets the start frequency in Hz"""
        return float(self._resource.query(":FREQ:STAR?"))

    @freq_start.setter
    def freq_start(self, freq_hz: float):
        """Sets the start frequency in Hz"""
        assert 0 <= freq_hz <= 3.2e9, "Start frequency must be between 0 and 3.2 GHz"
        self._resource.write(f":FREQ:STAR {freq_hz} Hz")

    @property
    def freq_stop(self) -> float:
        """Gets the stop frequency in Hz"""
        return float(self._resource.query(":FREQ:STOP?"))

    @freq_stop.setter
    def freq_stop(self, freq_hz: float):
        """Sets the stop frequency in Hz"""
        assert 0 <= freq_hz <= 3.2e9, "Stop frequency must be between 0 and 3.2 GHz"
        self._resource.write(f":FREQ:STOP {freq_hz} Hz")

    # ----- Power -----

    @property
    def attenuation(self) -> float:
        """Gets the current attenuation level in dB"""
        return float(self._resource.query(":POW:ATT?"))

    @attenuation.setter
    def attenuation(self, db: float):
        """Sets the attenuation level between 0 and 51 dB"""
        assert 0 <= db <= 51, "Attenuation must be between 0 and 51 dB"
        self._resource.write(f":POW:ATT {db}")

    @property
    def preamp(self) -> bool:
        """Gets the status of the internal preamp. Returns true if active"""
        return self._resource.query("POW:GAIN?").strip() == "1"

    @preamp.setter
    def preamp(self, enabled: bool):
        """Sets the internal preamp state to `enabled`"""
        self._resource.write(f":POW:GAIN {'ON' if enabled else 'OFF'}")

    # ----- Bandwidth -----

    @property
    def rbw(self) -> Bandwidth:
        """Gets the resolution bandwidth"""
        return Bandwidth(float(self._resource.query(":BWID?")))

    @rbw.setter
    def rbw(self, bw: Bandwidth):
        """Sets the resolution bandwidth"""
        self._resource.write(f":BWID {bw.value}")

    @property
    def vbw(self) -> Bandwidth:
        """Gets the video bandwidth"""
        return Bandwidth(float(self._resource.query(":BWID:VID?")))

    @vbw.setter
    def vbw(self, bw: Bandwidth):
        """Sets the video bandwidth"""
        self._resource.write(f":BWID:VID {bw.value}")

    @property
    def average_type(self) -> AverageType:
        """Gets the average type"""
        return AverageType(self._resource.query(":AVER:TYPE?").strip())

    @average_type.setter
    def average_type(self, type: AverageType):
        """Sets the average type"""
        self._resource.write(f":AVER:TYPE {type.value}")

    # ----- Trace -----

    @property
    def sweep_time(self) -> float:
        """Gets the current sweep time in seconds"""
        return float(self._resource.query(":SWE:TIME?"))

    @sweep_time.setter
    def sweep_time(self, time: float):
        """Sets the sweep time to a value from 450us to 1.5ks"""
        assert 450e-6 <= time <= 1.5e3, "Time must be between 450us and 1.5ks"
        self._resource.write(f":SWE:TIME {time}s")

    def sweep_restart(self):
        """Retsarts the current sweep"""
        self._resource.write(":INIT:REST")

    def trace(self, trace: int) -> np.ndarray:
        """
        Gets a numpy array of the value of `trace`
        `trace` is one of 1,2,3,4
        The units of this data is dependent of the current configuration.
        This will force a retrigger of the measurement and wait the sweep time
        before returning a result.
        """
        assert 1 <= trace <= 4, "Trace is either 1,2,3, or 4"
        self.sweep_restart()
        self.block_until_complete()
        res = self._resource.query(f"TRACE? {trace}").strip()
        return np.fromstring(res, sep=",")
