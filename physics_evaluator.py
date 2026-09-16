#!/usr/bin/env python3
"""Maxwell stress evaluator. Research tool, not a propulsion simulator."""
from __future__ import annotations
import warnings
from typing import Any, Dict, Optional, Tuple
import numpy as np

W_STAR = 0.08
C_LIGHT = 2.99792458e8
MU0 = 4.0e-7 * np.pi
EPS0 = 1.0 / (MU0 * C_LIGHT**2)


class MaxwellStressTensorEvaluator:
    def __init__(self, W_base: float = W_STAR, model: str = "star", chi_vac: float = 1.0):
        self.W_base = float(W_base)
        self.model = model
        self.chi_vac = float(chi_vac)
        if model == "M2":
            warnings.warn(
                "M2 model selected: uses frozen W(n)=W_base*exp(0.23*(n-3)). "
                "W<0.125 is a model-internal bound, not a no-ghost theorem.",
                RuntimeWarning,
                stacklevel=2,
            )

    def W(self, n: int = 3) -> float:
        if self.model == "M2":
            return self.W_base * np.exp(0.23 * (n - 3))
        return self.W_base

    @staticmethod
    def maxwell_stress_tensor(E: np.ndarray, B: np.ndarray) -> np.ndarray:
        E = np.asarray(E, dtype=float)
        B = np.asarray(B, dtype=float)
        assert E.shape[-1] == 3 and B.shape[-1] == 3
        E2 = np.sum(E * E, axis=-1)
        B2 = np.sum(B * B, axis=-1)
        EE = E[..., :, None] * E[..., None, :]
        BB = B[..., :, None] * B[..., None, :]
        eye = np.eye(3)
        sigma = EPS0 * (EE - 0.5 * E2[..., None, None] * eye)
        sigma += (1.0 / MU0) * (BB - 0.5 * B2[..., None, None] * eye)
        return sigma

    def informational_stress(self, info_field: np.ndarray, n: int = 3) -> np.ndarray:
        w = self.W(n) * self.chi_vac
        info_field = np.asarray(info_field, dtype=float)
        if info_field.shape[-1:] == (3,):
            amp = info_field
            dyad = amp[..., :, None] * amp[..., None, :]
            trace = np.trace(dyad, axis1=-2, axis2=-1)
            eye = np.eye(3)
            return w * (dyad - 0.5 * trace[..., None, None] * eye)
        eye = np.eye(3)
        return w * info_field[..., None, None] * eye

    def surface_force(self, stress, normals, areas) -> np.ndarray:
        traction = np.einsum("...ij,...j->...i", stress, normals)
        return np.sum(traction * areas[:, None], axis=0)

    def evaluate(self, E, B, normals, areas, info_field: Optional[np.ndarray] = None, n: int = 3) -> Dict[str, Any]:
        E = np.asarray(E, dtype=float)
        B = np.asarray(B, dtype=float)
        normals = np.asarray(normals, dtype=float)
        areas = np.asarray(areas, dtype=float)
        F_em = self.surface_force(self.maxwell_stress_tensor(E, B), normals, areas)
        if info_field is None:
            F_info = np.zeros(3)
        else:
            sigma_info = self.informational_stress(info_field, n=n)
            if sigma_info.ndim == 2:
                sigma_info = np.broadcast_to(sigma_info, (len(areas), 3, 3)).copy()
            F_info = self.surface_force(sigma_info, normals, areas)
        F_total = F_em + F_info
        null_ok = np.allclose(F_em, 0.0) if np.allclose(E, 0.0) and np.allclose(B, 0.0) else True
        return {
            "F_em": F_em,
            "F_info": F_info,
            "F_total": F_total,
            "W_used": self.W(n),
            "model": self.model,
            "null_test_ok": bool(null_ok),
            "warning": ("M2 exploratory" if self.model == "M2" else None),
        }


def make_unit_sphere_surface(n_theta: int = 16, n_phi: int = 32) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    theta = np.linspace(0, np.pi, n_theta + 1)
    phi = np.linspace(0, 2 * np.pi, n_phi + 1)
    dtheta = theta[1] - theta[0]
    dphi = phi[1] - phi[0]
    centroids, normals, areas = [], [], []
    for i in range(n_theta):
        for j in range(n_phi):
            th = 0.5 * (theta[i] + theta[i + 1])
            ph = 0.5 * (phi[j] + phi[j + 1])
            x = np.sin(th) * np.cos(ph)
            y = np.sin(th) * np.sin(ph)
            z = np.cos(th)
            centroids.append([x, y, z])
            normals.append([x, y, z])
            areas.append(np.sin(th) * dtheta * dphi)
    return np.array(centroids), np.array(normals), np.array(areas)


def _self_test() -> None:
    print("Running self-tests …")
    ev = MaxwellStressTensorEvaluator(model="star")
    cents, norms, areas = make_unit_sphere_surface(8, 16)
    out = ev.evaluate(np.zeros_like(cents), np.zeros_like(cents), norms, areas)
    assert np.allclose(out["F_total"], 0.0)
    print("  null test passed")
    E = np.zeros_like(cents); E[:, 0] = 1.0
    out = ev.evaluate(E, np.zeros_like(cents), norms, areas)
    assert np.allclose(out["F_em"], 0.0, atol=1e-10)
    print("  uniform-E closed-surface test passed")
    assert abs(ev.W() - 0.08) < 1e-15
    print("  W_star lock passed")
    print("All self-tests passed.")


if __name__ == "__main__":
    _self_test()
