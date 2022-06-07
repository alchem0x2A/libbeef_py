`libbeef_py`: simple python interface to BEEF-vdW ensemble calculations.

TL;DR

- Reconstruct the BEEF ensemble vector from VASP calculations
```python
from libbeef import beefens
from libbeef.utils import parse_beefens
# Read the ensemble en
bee, xc = parse_beefens("OUTCAR")
# Reconstruct the same order of BEEF ensembles
bee_calc = beefens(xc[-1], random_method="vasp")
# The python reconstructed ensemble and VASP outputs should be identical
print(bee_calc - bee[-1])
```