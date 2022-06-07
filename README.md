`libbeef_py`: simple python interface to BEEF-vdW ensemble calculations.

TL;DR

- Reconstruct the BEEF ensemble energies from VASP calculations
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

- Calculate the BEEF ensemble energies with arbitrary length
```python
# Continue from case above
# Get a new ensemble energies vector with size of 500, and using numpy's random
bee_new = beefens(xc[-1], random_method="python", random_vec_size=500)
```