#!/usr/bin/env python3
"""
richardson_extrapolation.py
---------------------------
Richardson extrapolation utilities for mesh-convergence studies
on the Coherence Drive residual-force pathway.

Given a sequence of observed quantities Q(h) obtained on successively
refined meshes (here controlled by integer depth n_aft), estimate:

  - observed order of accuracy p
  - continuum limit Q* (h -> 0)

Assumptions (documented, not hidden):
  - The leading error term is A * h^p + higher-order terms.
  - Refinement factor r is known (for depth-driven Sierpinski meshes
    we treat successive depths as an effective geometric refinement
    and report the observed p rather than assuming a classical h-halving).

This module is pure numerics. It does not generate meshes, solve BVPs,
or raise claim level. It is a Stage-2 analysis tool only.

Claim discipline (ADL-Governance):
  experimental_validation = false
  thrust_validated        = false
"""

from __future__ import annotations
from typing import Sequence, Dict, Any, Optional, Tuple
import numpy as np


def observed_order(
    Q_coarse: float,
    Q_medium: float,
    Q_fine: float,
    r: float = 2.0,
) -> float:
    """
    Estimate observed order of accuracy from three successive values.

        p = log( (Q_medium - Q_coarse) / (Q_fine - Q_medium) ) / log(r)

    Returns NaN if denominators vanish or signs are inconsistent
    (non-monotonic or noisy sequence).
    """
    num = Q_medium - Q_coarse
    den = Q_fine - Q_medium
    if abs(den) < 1e-30 or num * den <= 0:
        return float("nan")
    return float(np.log(abs(num / den)) / np.log(r))


def richardson_extrapolate(
    Q_coarse: float,
    Q_fine: float,
    p: float,
    r: float = 2.0,
) -> float:
    """
    Two-point Richardson extrapolation to continuum limit.

        Q* = (r^p * Q_fine - Q_coarse) / (r^p - 1)
    """
    rp = r ** p
    if abs(rp - 1.0) < 1e-15:
        return float("nan")
    return (rp * Q_fine - Q_coarse) / (rp - 1.0)


def extrapolate_sequence(
    values: Sequence[float],
    refinement_ratio: float = 2.0,
    assumed_order: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Apply Richardson analysis to a monotonic refinement sequence.
    """
    vals = [float(v) for v in values]
    n = len(vals)
    rel_changes = []
    for i in range(1, n):
        denom = abs(vals[i - 1]) + 1e-30
        rel_changes.append(abs(vals[i] - vals[i - 1]) / denom)

    observed = []
    for i in range(n - 2):
        p = observed_order(vals[i], vals[i + 1], vals[i + 2], r=refinement_ratio)
        observed.append(p)

    if assumed_order is not None:
        p_used = float(assumed_order)
    elif observed and not np.isnan(observed[-1]):
        p_used = observed[-1]
    else:
        p_used = float("nan")

    if n >= 2 and not np.isnan(p_used):
        Q_star = richardson_extrapolate(vals[-2], vals[-1], p_used, r=refinement_ratio)
    else:
        Q_star = float("nan")

    notes = [
        "Richardson assumes a single dominant error term A*h^p.",
        "Depth-driven Sierpinski refinement is anisotropic; r is effective.",
        "Piecewise-constant collocation BEM is typically first-order (p~1).",
        "NaN order or Q* indicates non-monotonic or insufficient data.",
        "This is a numerical diagnostic only — not a physical validation.",
    ]

    return {
        "values": vals,
        "observed_orders": observed,
        "p_used": p_used,
        "Q_star": Q_star,
        "relative_changes": rel_changes,
        "refinement_ratio": refinement_ratio,
        "notes": notes,
    }


def vector_extrapolate(
    vectors: Sequence[np.ndarray],
    refinement_ratio: float = 2.0,
    assumed_order: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Component-wise Richardson on a sequence of 3-vectors (e.g. force).
    Also reports direction stability (successive unit-vector dots).
    """
    vecs = [np.asarray(v, dtype=float).ravel()[:3] for v in vectors]
    components = []
    for c in range(3):
        seq = [v[c] for v in vecs]
        components.append(extrapolate_sequence(seq, refinement_ratio, assumed_order))

    dirs = []
    for v in vecs:
        nrm = np.linalg.norm(v) + 1e-30
        dirs.append(v / nrm)
    dir_dots = []
    for i in range(1, len(dirs)):
        dir_dots.append(float(np.dot(dirs[i - 1], dirs[i])))

    Q_star_vec = np.array([c["Q_star"] for c in components])
    return {
        "components": components,
        "Q_star_vector": Q_star_vec,
        "|Q_star|": float(np.linalg.norm(Q_star_vec)),
        "direction_dots": dir_dots,
        "unit_directions": dirs,
    }


def _self_test() -> None:
    print("richardson_extrapolation self-test …")
    hs = [1.0, 0.5, 0.25]
    Qs = [1.0 + 2 * h + 3 * h ** 2 for h in hs]
    res = extrapolate_sequence(Qs, refinement_ratio=2.0)
    print(f"  values          = {res['values']}")
    print(f"  observed_orders = {res['observed_orders']}")
    print(f"  p_used          = {res['p_used']:.4f}")
    print(f"  Q_star          = {res['Q_star']:.6f}  (expect ~1)")
    assert abs(res["Q_star"] - 1.0) < 0.15, "extrapolation far from continuum"
    print("  self-test passed (within expected higher-order pollution).")


if __name__ == "__main__":
    _self_test()
