"""Classical-first surface diagnostics. No Ware term is introduced here."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from physics_evaluator import MaxwellStressTensorEvaluator, make_unit_sphere_surface


@dataclass
class DualSurfaceResult:
    F_inner: np.ndarray
    F_outer: np.ndarray
    epsilon_surface: float
    F_even_norm: float
    closed: bool


def _sphere(radius: float, n_theta: int, n_phi: int):
    cents, norms, areas = make_unit_sphere_surface(n_theta, n_phi)
    cents = cents * radius
    areas = areas * (radius ** 2)
    return cents, norms, areas


def uniform_E_two_surface(E0=(1.0, 0.0, 0.0), r1=1.0, r2=2.0, n_theta=12, n_phi=24) -> DualSurfaceResult:
    ev = MaxwellStressTensorEvaluator(model="star")
    Ehat = np.asarray(E0, dtype=float)
    results = []
    for R in (r1, r2):
        cents, norms, areas = _sphere(R, n_theta, n_phi)
        E = np.broadcast_to(Ehat, cents.shape).copy()
        B = np.zeros_like(E)
        out = ev.evaluate(E, B, norms, areas)
        results.append(out["F_em"])
    Fi, Fo = results
    denom = max(np.linalg.norm(Fi), np.linalg.norm(Fo), 1e-18)
    eps = float(np.linalg.norm(Fi - Fo) / denom) if denom else 0.0
    closed = np.linalg.norm(Fi) < 1e-8 and np.linalg.norm(Fo) < 1e-8
    return DualSurfaceResult(Fi, Fo, eps, float(np.linalg.norm(0.5 * (Fi + Fo))), closed)


def mesh_epsilon(F_h: np.ndarray, F_h2: np.ndarray, floor: float = 1e-18) -> float:
    denom = max(np.linalg.norm(F_h), np.linalg.norm(F_h2), floor)
    return float(np.linalg.norm(F_h2 - F_h) / denom)
