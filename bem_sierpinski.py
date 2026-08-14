#!/usr/bin/env python3
"""
bem_sierpinski.py
-----------------
Quasi-static electromagnetic boundary-value problem on the
0.45 asymmetric Sierpinski tetrahedron.

Method: collocation BEM for a conducting surface in an external
uniform electric field. Surface charge σ is solved from

    φ_ext(r) + (1/(4πϵ0)) ∫ σ(r')/|r-r'| dA' = V_const

then the electrostatic pressure (σ²/(2ϵ0)) is integrated.

This is a real BVP, not a synthetic field proxy.

Limitations
-----------
- Electrostatics only (no magnetics / radiation).
- Piecewise-constant σ per triangle; centroid collocation.
- Self-term regularised by equivalent-disk approximation.
- Net force on a closed conductor in uniform E is theoretically
  zero; residual measures mesh asymmetry + discretisation error.
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


def mesh_elements(V, F):
    cents, norms, areas = [], [], []
    for i0, i1, i2 in F:
        v0, v1, v2 = V[i0], V[i1], V[i2]
        c = (v0 + v1 + v2) / 3.0
        n = np.cross(v1 - v0, v2 - v0)
        a = np.linalg.norm(n)
        if a < 1e-18:
            continue
        n = n / a
        cents.append(c)
        norms.append(n)
        areas.append(0.5 * a)
    return np.array(cents), np.array(norms), np.array(areas)


def bem_solve_conductor(cents, norms, areas, E_inf, V0=0.0):
    N = len(cents)
    phi_ext = -cents @ E_inf
    G = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            if i == j:
                R_eq = np.sqrt(areas[j] / np.pi)
                G[i, j] = areas[j] / (R_eq + 1e-30) * 0.5
            else:
                d = np.linalg.norm(cents[i] - cents[j])
                G[i, j] = areas[j] / (d + 1e-30)
    rhs = 4.0 * np.pi * EPS0 * (V0 - phi_ext)
    return np.linalg.solve(G + 1e-12 * np.eye(N), rhs)


def maxwell_stress_force(normals, areas, sigma):
    pressure = (sigma ** 2) / (2.0 * EPS0)
    return np.sum((pressure * areas)[:, None] * normals, axis=0)


def run(n_aft=2, n_fore=1, E0=1.0):
    V, F = generate_asymmetric_sierpinski(alpha=0.45, n_aft=n_aft, n_fore=n_fore)
    cents, norms, areas = mesh_elements(V, F)
    E_inf = np.array([0.0, 0.0, E0])
    sigma = bem_solve_conductor(cents, norms, areas, E_inf)
    F_net = maxwell_stress_force(norms, areas, sigma)
    return {
        "n_aft": n_aft,
        "n_faces": len(areas),
        "Q_total": float(np.sum(sigma * areas)),
        "F_net": F_net,
        "|F|": float(np.linalg.norm(F_net)),
        "direction": F_net / (np.linalg.norm(F_net) + 1e-30),
        "sigma_rms": float(np.sqrt(np.mean(sigma ** 2))),
    }


def main():
    print("=" * 60)
    print("BEM electrostatic BVP on asymmetric Sierpinski (α=0.45)")
    print("=" * 60)
    results = []
    for n_aft in (1, 2, 3):
        r = run(n_aft=n_aft)
        results.append(r)
        print(f"\nn_aft={n_aft}  faces={r['n_faces']}")
        print(f"  |F_net|   = {r['|F|']:.6e} N")
        print(f"  direction = {r['direction']}")
    dirs = np.array([r["direction"] for r in results])
    print("\nDirectional stability:")
    for i in range(1, len(dirs)):
        print(f"  {results[i-1]['n_aft']}→{results[i]['n_aft']}: "
              f"{np.dot(dirs[i-1], dirs[i]):.4f}")
    print("\nReal BVP; electrostatics only; RF/magnetics open.")
    print("=" * 60)


if __name__ == "__main__":
    main()
