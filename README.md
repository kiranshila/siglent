# siglent

A modern python library for interacting with Siglent-brand test equipment

## Examaple

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
sa.rbw = Bandwidth.MHZ_1
sa.vbw = Bandwidth.KHZ_100
sa.attenuation = 0
sa.preamp = True

# Measure
trace = sa.trace(1)
```
