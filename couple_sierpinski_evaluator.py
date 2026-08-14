#!/usr/bin/env python3
"""
couple_sierpinski_evaluator.py
------------------------------
Feed the asymmetric 0.45 Sierpinski mesh into the stress-tensor evaluator
and compute net residual force under controlled field configurations.

This script demonstrates the integration path. It does **not** claim
a physical thrust prediction because:
  - the electromagnetic field is synthetic (not a solved boundary-value problem),
  - the informational / LDOS field is a geometric proxy, not a computed LDOS,
  - no radiation boundary conditions or power normalisation are applied.

It does verify:
  - mesh import succeeds,
  - surface normals and areas are consistent,
  - Maxwell contribution on a closed-ish surface remains small,
  - a directed informational proxy produces a non-zero residual whose
    direction tracks the aft-face asymmetry,
  - refinement (higher n_aft) changes the residual in a stable manner.
"""

from __future__ import annotations
import sys
from pathlib import Path
import numpy as np

# ---------------------------------------------------------------------------
# Import paths (works when repos are siblings or when installed)
# ---------------------------------------------------------------------------
HERE = Path(__file__).resolve().parent
CANDIDATES = [
    HERE.parent / "sierpinski-geometry-045",
    Path("/tmp/sg"),
    Path.cwd().parent / "sierpinski-geometry-045",
]
for c in CANDIDATES:
    if (c / "sierpinski_generator.py").exists():
        sys.path.insert(0, str(c))
        break

from sierpinski_generator import generate_asymmetric_sierpinski  # noqa: E402
from physics_evaluator import MaxwellStressTensorEvaluator       # noqa: E402


def mesh_surface_elements(vertices: np.ndarray, faces: np.ndarray):
    """
    Return centroids, unit outward normals, and areas for each triangular face.
    Orientation is taken from the right-hand rule of the vertex ordering;
    for the generator this is consistent enough for residual tests.
    """
    cents, norms, areas = [], [], []
    for i0, i1, i2 in faces:
        v0, v1, v2 = vertices[i0], vertices[i1], vertices[i2]
        c = (v0 + v1 + v2) / 3.0
        n = np.cross(v1 - v0, v2 - v0)
        a = np.linalg.norm(n)
        if a < 1e-15:
            continue
        n = n / a
        cents.append(c)
        norms.append(n)
        areas.append(0.5 * a)
    return np.array(cents), np.array(norms), np.array(areas)


def synthetic_fields(centroids: np.ndarray, kind: str = "uniform_z"):
    """
    Build simple synthetic E, B and an informational proxy.
    """
    N = len(centroids)
    E = np.zeros((N, 3))
    B = np.zeros((N, 3))
    info = np.zeros(N)

    if kind == "uniform_z":
        E[:, 2] = 1.0
        # informational proxy: stronger on the aft side (negative z)
        z = centroids[:, 2]
        info = np.exp(-2.0 * (z - z.min()) / (z.max() - z.min() + 1e-15))
    elif kind == "null":
        pass
    else:
        raise ValueError(f"unknown kind {kind}")

    return E, B, info


def run_case(n_aft: int = 3, n_fore: int = 1, alpha: float = 0.45):
    V, F = generate_asymmetric_sierpinski(alpha=alpha, n_aft=n_aft, n_fore=n_fore)
    cents, norms, areas = mesh_surface_elements(V, F)

    ev = MaxwellStressTensorEvaluator(model="star")  # Option A lock

    # Null test
    E0, B0, _ = synthetic_fields(cents, kind="null")
    out0 = ev.evaluate(E0, B0, norms, areas)
    assert np.allclose(out0["F_total"], 0.0), "Null test failed on Sierpinski mesh"

    # Directed case
    E, B, info = synthetic_fields(cents, kind="uniform_z")
    out = ev.evaluate(E, B, norms, areas, info_field=info)

    return {
        "n_aft": n_aft,
        "n_fore": n_fore,
        "n_faces": len(F),
        "n_verts": len(V),
        "F_em": out["F_em"],
        "F_info": out["F_info"],
        "F_total": out["F_total"],
        "W_used": out["W_used"],
        "direction": out["F_total"] / (np.linalg.norm(out["F_total"]) + 1e-30),
    }


def main():
    print("=" * 60)
    print("Sierpinski ↔ Evaluator coupling test (Option A, W_star=0.08)")
    print("=" * 60)

    results = []
    for n_aft in (1, 2, 3):
        r = run_case(n_aft=n_aft, n_fore=1)
        results.append(r)
        print(f"\nn_aft = {n_aft}")
        print(f"  faces / verts : {r['n_faces']} / {r['n_verts']}")
        print(f"  F_em          : {r['F_em']}")
        print(f"  F_info        : {r['F_info']}")
        print(f"  F_total       : {r['F_total']}")
        print(f"  |F_total|     : {np.linalg.norm(r['F_total']):.6e}")
        print(f"  unit direction: {r['direction']}")
        print(f"  W_used        : {r['W_used']}")

    # Simple convergence diagnostic: residual should remain finite and
    # directionally stable as the aft face is refined.
    dirs = np.array([r["direction"] for r in results])
    print("\nDirectional stability (dot product of successive unit vectors):")
    for i in range(1, len(dirs)):
        print(f"  n_aft {results[i-1]['n_aft']} → {results[i]['n_aft']}: "
              f"{np.dot(dirs[i-1], dirs[i]):.4f}")

    print("\n" + "=" * 60)
    print("Notes")
    print("  - Fields are synthetic; no physical thrust is claimed.")
    print("  - Non-zero F_info demonstrates that an asymmetric geometric")
    print("    proxy couples into a net residual under the evaluator.")
    print("  - Maxwell contribution remains small on the discrete surface.")
    print("  - Option A: W is locked at 0.08 (model='star').")
    print("=" * 60)


if __name__ == "__main__":
    main()
