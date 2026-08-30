#!/usr/bin/env python3
"""
fullwave_bem.py
---------------
Frequency-domain EFIE-style BEM on the 0.45 asymmetric Sierpinski surface
using the free-space radiating Helmholtz Green's function.

What this computes
------------------
- Piecewise-constant face currents (not RWG)
- Radiated-power proxy from 1/2 Re(I* Z I)
- Far-field pattern asymmetry factor A from a simple equivalent-source
  radiation estimate (Class B observable, estimated)

What this does NOT claim
------------------------
- Laboratory thrust validation
- Reactionless closed-system force
- Converged dual-surface Maxwell epsilon_F residual
- Production MLFMA / RWG accuracy

Force on the surface using 1/2 mu0 |I|^2 pressure is a DIAGNOSTIC only;
prefer far-field momentum flux for Class B accounting.
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

C = 2.99792458e8
MU0 = 4e-7 * np.pi
ETA0 = np.sqrt(MU0 / 8.854187817e-12)


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


def helmholtz_G(R, k):
    R = np.maximum(R, 1e-15)
    return np.exp(-1j * k * R) / (4 * np.pi * R)


def efie_matrix(cents, areas, k):
    N = len(cents)
    Z = np.zeros((N, N), dtype=complex)
    for i in range(N):
        for j in range(N):
            if i == j:
                Rself = np.sqrt(areas[j] / np.pi)
                Gself = 1.0 / (4 * np.pi * Rself) * (1 - 1j * k * Rself)
                Z[i, j] = 1j * k * ETA0 * Gself * areas[i] * areas[j]
            else:
                R = np.linalg.norm(cents[i] - cents[j])
                Z[i, j] = 1j * k * ETA0 * helmholtz_G(R, k) * areas[i] * areas[j]
    return Z


def far_field_asymmetry(cents, areas, I, k, n_ang=80, R_far=50.0):
    """Approximate pattern A = int n|f|^2 / int |f|^2 from face sources."""
    i = np.arange(n_ang)
    y = 1 - 2 * i / max(n_ang - 1, 1)
    rxy = np.sqrt(np.maximum(0, 1 - y * y))
    phi = np.pi * (3 - np.sqrt(5)) * i
    dirs = np.column_stack([rxy * np.cos(phi), y, rxy * np.sin(phi)])
    far = R_far * dirs
    w = 4 * np.pi / n_ang
    psi = np.zeros(n_ang, dtype=complex)
    for c, a, cur in zip(cents, areas, I):
        r = np.maximum(np.linalg.norm(far - c, axis=1), 1e-8)
        psi += cur * a * np.exp(1j * k * r) / (4 * np.pi * r)
    f = R_far * np.exp(-1j * k * R_far) * psi
    pw = np.abs(f) ** 2
    P = float(np.sum(pw * w))
    Fvec = np.array([float(np.sum(dirs[:, j] * pw * w)) for j in range(3)])
    A = Fvec / (P + 1e-30)
    return {
        "|A|": float(np.linalg.norm(A)),
        "A": A.tolist(),
        "note": "estimated pattern asymmetry; not validated F/P",
    }


def solve_fullwave(n_aft=2, n_fore=1, freq=1e9, E0=1.0):
    V, F = generate_asymmetric_sierpinski(0.45, n_aft, n_fore)
    cents, norms, areas = mesh_elements(V, F)
    k = 2 * np.pi * freq / C
    k_hat = np.array([0.0, 0.0, 1.0])
    E0_vec = np.array([E0, 0.0, 0.0])
    Z = efie_matrix(cents, areas, k)
    phase = np.exp(-1j * k * (cents @ k_hat))
    Vvec = np.zeros(len(cents), dtype=complex)
    for i in range(len(cents)):
        E = E0_vec * phase[i]
        Et = E - (E @ norms[i]) * norms[i]
        Vvec[i] = np.linalg.norm(Et) + 0j
    I = np.linalg.solve(Z + 1e-12 * np.eye(len(cents)), Vvec)

    pressure = 0.5 * MU0 * np.abs(I) ** 2
    F_diag = np.sum((pressure * areas)[:, None] * norms, axis=0)
    Prad = 0.5 * np.real(np.vdot(I, Z @ I))
    A_info = far_field_asymmetry(cents, areas, I, k)

    return {
        "n_faces": len(areas),
        "freq_Hz": freq,
        "ka_char": float(k * np.max(np.linalg.norm(cents, axis=1))),
        "|I|_rms": float(np.sqrt(np.mean(np.abs(I) ** 2))),
        "F_surface_diagnostic": F_diag.tolist(),
        "|F|_surface_diagnostic": float(np.linalg.norm(F_diag)),
        "P_rad_proxy": float(Prad),
        "pattern_asymmetry": A_info,
        "claim_flags": {
            "thrust_validated": False,
            "experimental_validation": False,
            "reactionless_closed_thrust": False,
            "epsilon_F_reported": False,
        },
        "limits": (
            "PEC; dense EFIE; piecewise-constant unknowns; "
            "surface pressure force is diagnostic only; "
            "use pattern_asymmetry as estimated Class B A; "
            "dual-surface Maxwell epsilon_F not implemented"
        ),
    }


def main():
    print("=" * 60)
    print("Full-wave EFIE BEM (radiating Helmholtz kernel)")
    print("Research diagnostic — not a thrust claim")
    print("=" * 60)
    for n_aft in (1, 2, 3):
        for freq in (1e8, 1e9):
            r = solve_fullwave(n_aft=n_aft, freq=freq)
            print(f"n_aft={n_aft} f={freq:.0e} faces={r['n_faces']} ka={r['ka_char']:.3f}")
            print(f"  |F|_surface_diag={r['|F|_surface_diagnostic']:.4e} (diagnostic only)")
            print(f"  P_rad_proxy={r['P_rad_proxy']:.4e}")
            print(f"  |A|_pattern={r['pattern_asymmetry']['|A|']:.4e} (estimated)")
    print("Radiating kernel; PEC; dense EFIE. Not RWG/MLFMA.")
    print("thrust_validated=false  epsilon_F not reported")
    print("=" * 60)


if __name__ == "__main__":
    main()
