"""Calculate BEEF-vdW ensemble energies 
"""
import numpy as np
import warnings
from .constants import (
    BEEFMAT,
    BEEFMAT_SIZE,
    RANDVEC_2000,
    RANDOM_SEED,
    DEFAULT_RANDVEC_SIZE,
)


def gen_coeff_vec(rand_vec=RANDVEC_2000, beef_ensemble_matrix=BEEFMAT):
    """Generate the BEEF ensemble coefficient vectors
    a = Dot(M, rand_vec)
    where M is the BEEF ensemble matrix
    """
    rand_vec = np.array(rand_vec).astype(np.float64)
    beef_ensemble_matrix = np.array(beef_ensemble_matrix).astype(np.float64)
    matrix_m, matrix_n = beef_ensemble_matrix.shape
    if matrix_m != matrix_n:
        raise ValueError("BEEF ensemble matrix must be square!")
    vec_m, vec_n = rand_vec.shape
    if vec_m != matrix_m:
        if vec_n != matrix_m:
            raise ValueError("Input random vector shape is incorrect!")
        else:
            rand_vec = rand_vec.T
            warnings.warn(
                f"Input random vector seems to be {vec_m} X {vec_n}, applied transposition."
            )
    a_vec = np.dot(beef_ensemble_matrix, rand_vec)
    # Output shape of a_vec will have size (matrix_m + 1) x matrix_n
    # a_vec_out[-1, i] = -a_vec[-1, i]
    a_vec_out = np.vstack([a_vec, -a_vec[-1]])
    return a_vec_out


def gen_ensemble_energies(beefxc, coeff_vec):
    """Calculate ensemble energies using formula
    E_ens = Dot(beefxc, coeff_vec)
    N           M+1     M+1 x N
    """
    # beefxc = np.ravel(np.array(beefxc).astype(np.float64))
    (xc_size,) = beefxc.shape
    coeff_vec = np.array(coeff_vec).astype(np.float64)
    vec_m, vec_n = coeff_vec.shape
    if vec_m != xc_size:
        if vec_n != xc_size:
            raise ValueError("Input coefficient vector shape does not match beefxc")
        else:
            rand_vec = rand_vec.T
            warnings.warn(
                f"Input coefficient vector seems to be {vec_m} X {vec_n}, applied transposition."
            )

    ens = np.dot(beefxc, coeff_vec)
    return ens


def beefens(
    beefxc,
    beef_ensemble_matrix=BEEFMAT,
    random_method="vasp",
    random_vec_size=DEFAULT_RANDVEC_SIZE,
    seed=RANDOM_SEED,
):
    """Wrapper of the beefens calculation.
    beefxc is the given xc contributions from a BEEF-vdW calculation
    random_method can be either "vasp" or "python".
    random_vec_size and seed only affect when choosing python as randvec generator
    """
    random_method = random_method.lower()
    beefxc = np.ravel(np.array(beefxc).astype(np.float64))
    (xc_size,) = beefxc.shape
    vec_m = xc_size - 1
    if random_method not in ("vasp", "python"):
        raise ValueError("Please choose random_method either as 'vasp' or 'python'")
    if random_method == "vasp":
        rand_vec = RANDVEC_2000
    else:
        np.random.seed(seed)
        # Generate sampling from N(0, 1)
        rand_vec = np.random.normal(loc=0.0, scale=1.0, size=(vec_m, random_vec_size))
    coeff_vec = gen_coeff_vec(rand_vec, beef_ensemble_matrix)
    E_ens = gen_ensemble_energies(beefxc, coeff_vec)
    return E_ens
