"""Parse VASP OUTCAR files
"""
import re
from os.path import join
from pathlib import Path

import numpy as np
from monty.io import zopen


def parse_beefens(outcar, images=":"):
    """Parse the BEEFENS and XC contributions from OUTCAR
    By default returns all images results
    """
    filename = Path(outcar).as_posix()
    with zopen(filename, "rt") as f:
        lines = f.readlines()
    # Ensemble energies
    header = "BEEFens 2000 ensemble energies"
    E_ens = []
    max_lines = len(lines)
    for i, line in enumerate(lines):
        part_lines = []
        if header in line:
            for delta in range(1, 2001):
                lnum = i + delta
                if lnum < max_lines:
                    part_lines.append(float(lines[lnum].strip()))
                else:
                    part_lines = None
                    break
        if part_lines:
            part_lines = np.array(part_lines)
            assert part_lines.shape[0] == 2000
            E_ens.append(np.array(part_lines))
    # XC contributions
    header = "BEEF xc energy contributions"
    XC_contrib = []
    max_lines = len(lines)
    for i, line in enumerate(lines):
        part_lines = []
        if header in line:
            for delta in range(1, 33):
                lnum = i + delta
                if lnum < max_lines:
                    part_lines.append(float(lines[lnum].strip().split(":")[1]))
                else:
                    part_lines = None
                    break
        if part_lines:
            part_lines = np.array(part_lines)
            assert part_lines.shape[0] == 32
            XC_contrib.append(np.array(part_lines))
    # add support for image selection
    return E_ens, XC_contrib
