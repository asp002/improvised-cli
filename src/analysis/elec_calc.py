from functools import lru_cache

import numpy as np

from .pot_extract import extract
from .pot_val import val_potential as U


@lru_cache(maxsize=None)
def compute_field(filepath):

    if not compute_field.cache_info().hits:
        print("Generating Field data. ")

    xmin, ymin, zmin, hx, hy, hz, nx, ny, nz = extract(filepath)

    _x = np.linspace(0, 2, nx)
    _y = np.linspace(0, 3, ny)
    _z = np.linspace(0, 4, nz)
    X, Y, Z = np.meshgrid(_x, _y, _z, indexing="ij")

    # Vectorize the U function
    U_vectorized = np.vectorize(U)

    # Compute the potential at each grid point
    potentials = U_vectorized(X, Y, Z, filepath)

    # Compute the gradient of the potential field
    grad_x, grad_y, grad_z = np.gradient(potentials)
    # Compute the electric field
    Ex, Ey, Ez = -grad_x, -grad_y, -grad_z
    # Ex, Ey, Ez = grad_x, grad_y, grad_z

    if not compute_field.cache_info().hits:
        print("Field generation successful.")

    return Ex, Ey, Ez


def elec(cx, cy, cz, filepath):
    Ex, Ey, Ez = compute_field(filepath)
    field = Ex[cx, cy, cz], Ey[cx, cy, cz], Ez[cx, cy, cz]
    return field
