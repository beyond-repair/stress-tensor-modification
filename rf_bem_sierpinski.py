#!/usr/bin/env python3
"""
rf_bem_sierpinski.py
--------------------
Promotion of the electrostatic BEM toward RF / magnetostatic regimes
on the 0.45 asymmetric Sierpinski surface.

1. Electrostatic: conducting surface in uniform E.
2. Magnetostatic: thin-shell Neumann problem in uniform B.
3. Quasi-static RF: Leontovich impedance BC at given ω.

Not a full-wave 3D Maxwell solver with radiation BCs.
"""

from __future__ import annotations
import sys
from pathlib import Path
import numpy as np

for c in [Path("/tmp/sg"),
          Path.cwd().parent / "sierpinski-geometry-045",
          Path(__file__).resolve().parent.parent / "sierpinski-geometry-045"]:
    if (c / "sierpinski_generator.py").exists():
        sys.path.insert(0, str(c))
        break

from sierpinski_generator import generate_asymmetric_sierpinski

EPS0 = 8.854187817e-12
MU0 = 4e-7 * np.pi


def mesh_elements(V, F):
    cents, norms, areas = [], [], []
    for i0, i1, i2 in F:
        v0, v1, v2 = V[i0], V[i1], V[i2]
        c = (v0 + v1 + v2) / 3.0
        n = np.cross(v1 - v0, v2 - v0)
        a = np.linalg.norm(n)
        if a < 1e-18:
            continue
        cents.append(c)
        norms.append(n / a)
        areas.append(0.5 * a)
    return np.array(cents), np.array(norms), np.array(areas)


def _G_matrix(cents, areas):
    N = len(cents)
    G = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            if i == j:
                R = np.sqrt(areas[j] / np.pi)
                G[i, j] = 0.5 * areas[j] / (R + 1e-30)
            else:
                G[i, j] = areas[j] / (np.linalg.norm(cents[i] - cents[j]) + 1e-30)
    return G


def bem_electrostatic(cents, areas, E_inf, V0=0.0):
    G = _G_matrix(cents, areas)
    phi_ext = -cents @ E_inf
    rhs = 4 * np.pi * EPS0 * (V0 - phi_ext)
    return np.linalg.solve(G + 1e-12 * np.eye(len(cents)), rhs)


def force_electrostatic(normals, areas, sigma):
    p = sigma**2 / (2 * EPS0)
    return np.sum((p * areas)[:, None] * normals, axis=0)


def bem_magnetostatic(cents, norms, areas, B_inf):
    G = _G_matrix(cents, areas)
    rhs = -(norms @ B_inf) * areas
    eta = np.linalg.solve(G + 1e-12 * np.eye(len(cents)), rhs)
    B_loc2 = (B_inf @ B_inf) + (eta / (areas + 1e-30))**2
    pressure = B_loc2 / (2 * MU0)
    F = np.sum((pressure * areas)[:, None] * norms, axis=0)
    return eta, F


def bem_rf_quasistatic(cents, norms, areas, E_inf, omega, sigma_cond=1e7):
    N = len(cents)
    Zs = (1 + 1j) * np.sqrt(omega * MU0 / (2 * sigma_cond))
    G = _G_matrix(cents, areas).astype(complex)
    E_tang = np.zeros(N, dtype=complex)
    for i in range(N):
        Et = E_inf - (E_inf @ norms[i]) * norms[i]
        E_tang[i] = np.linalg.norm(Et) + 0j
    A = (1j * omega * MU0 / (4 * np.pi)) * G + Zs * np.eye(N)
    K = np.linalg.solve(A, E_tang)
    pressure = 0.5 * MU0 * np.abs(K)**2
    F = np.sum((pressure * areas)[:, None] * norms, axis=0)
    return K, F


def run_all(n_aft=2, n_fore=1):
    V, F = generate_asymmetric_sierpinski(0.45, n_aft, n_fore)
    cents, norms, areas = mesh_elements(V, F)
    E_inf = np.array([0.0, 0.0, 1.0])
    B_inf = np.array([0.0, 0.0, 1.0])
    sigma = bem_electrostatic(cents, areas, E_inf)
    Fe = force_electrostatic(norms, areas, sigma)
    _, Fm = bem_magnetostatic(cents, norms, areas, B_inf)
    _, Frf = bem_rf_quasistatic(cents, norms, areas, E_inf, omega=2*np.pi*1e9)
    return {
        "n_faces": len(areas),
        "|Fe|": np.linalg.norm(Fe), "dir_e": Fe/(np.linalg.norm(Fe)+1e-30),
        "|Fm|": np.linalg.norm(Fm), "dir_m": Fm/(np.linalg.norm(Fm)+1e-30),
        "|Frf|": np.linalg.norm(Frf), "dir_rf": Frf/(np.linalg.norm(Frf)+1e-30),
    }


def main():
    print("=" * 60)
    print("RF / Magnetostatic BEM on Sierpinski α=0.45")
    print("=" * 60)
    for n_aft in (1, 2, 3):
        r = run_all(n_aft=n_aft)
        print(f"\nn_aft={n_aft}  faces={r['n_faces']}")
        print(f"  |Fe|={r['|Fe|']:.4e}  dir={r['dir_e']}")
        print(f"  |Fm|={r['|Fm|']:.4e}  dir={r['dir_m']}")
        print(f"  |Frf|={r['|Frf|']:.4e} dir={r['dir_rf']}")
    print("\nQuasi-static / thin-shell only. Full-wave radiation BC open.")
    print("=" * 60)


if __name__ == "__main__":
    main()
