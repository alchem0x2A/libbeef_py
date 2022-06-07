"""Calculate BEEF-vdW ensemble energies 
"""
import numpy as np
import warnings
from .constants import BEEFMAT, BEEFMAT_SIZE, RANDVEC_2000

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
            warnings.warn(f"Input random vector seems to be {vec_m} X {vec_n}, applied transposition.")
    a_vec = np.dot(beef_ensemble_matrix, rand_vec)
    return a_vec