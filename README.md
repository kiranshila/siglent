# siglent

A modern python library for interacting with Siglent-brand test equipment.

## Installation

Until published, install with

```sh
pip install -e git+https://github.com/kiranshila/siglent#egg=siglent
```

Note: This requires at least Pip 19.0

## Example

```python
from pyvisa import ResourceManager
from siglent.spectrum_analyzers import SSA3000X, Bandwidth

rm = ResourceManager()
sa = SSA3000X("TCPIP0::192.168.1.125::inst0::INSTR", rm)

# Preset
sa.reset()

# Setup
sa.span = 500e6
sa.freq_center = 2.4e9
sa.rbw = Bandwidth(1e6)
sa.vbw = Bandwidth(100e3)
sa.attenuation = 0
sa.preamp = True

# Measure
trace = sa.trace(1).data
```
