#!/usr/bin/env python3
"""
physics_evaluator.py
--------------------
Mesh-aware evaluator for the modified stress tensor

    T_eff^{ij} = T_EM^{ij} + W * chi_vac * (informational contribution)

Locked default: W_star = 0.08.

The informational contribution is supplied by the caller as a scalar or
vector field sampled on the same mesh (e.g. an LDOS proxy). This module
does **not** invent an LDOS; it only contracts the supplied field with the
Maxwell stress and integrates.

Guardrails:
  - Default model is "star" (W = 0.08 constant).
  - Model "M2" is available but emits a runtime warning because the
    tabulated values violate the earlier ghost-free bound W < 0.125.
  - All returned forces are computed from the supplied fields; zero input
    fields produce zero force (null test).

This is a research tool, not a production propulsion simulator.
"""

from __future__ import annotations
import warnings
from typing import Dict, Any, Optional, Tuple
import numpy as np

# ---------------------------------------------------------------------------
# Constants / Symbol Registry alignment
# ---------------------------------------------------------------------------
W_STAR = 0.08          # locked phenomenological anchor
C_LIGHT = 2.99792458e8 # m/s
MU0 = 4.0e-7 * np.pi   # H/m
EPS0 = 1.0 / (MU0 * C_LIGHT**2)


class MaxwellStressTensorEvaluator:
    """
    Evaluate net force from Maxwell stress + optional Ware/informational term.
    """

    def __init__(
        self,
        W_base: float = W_STAR,
        model: str = "star",
        chi_vac: float = 1.0,
    ):
        """
        Parameters
        ----------
        W_base : float
            Base Ware factor. Default is the locked W_star = 0.08.
        model : {"star", "M2"}
            "star" keeps W constant at W_base.
            "M2" applies the provisional exponential (emits warning).
        chi_vac : float
            Vacuum susceptibility prefactor (dimensionless placeholder).
        """
        self.W_base = float(W_base)
        self.model = model
        self.chi_vac = float(chi_vac)

        if model == "M2":
            warnings.warn(
                "M2 model selected: tabulated W(n) values exceed the earlier "
                "ghost-free bound W < 0.125. Treat results as exploratory only.",
                RuntimeWarning,
                stacklevel=2,
            )

    # ------------------------------------------------------------------
    def W(self, n: int = 3) -> float:
        if self.model == "M2":
            return self.W_base * np.exp(0.23 * (n - 1))
        return self.W_base

    # ------------------------------------------------------------------
    @staticmethod
    def maxwell_stress_tensor(
        E: np.ndarray,
        B: np.ndarray,
    ) -> np.ndarray:
        """
        Classical Maxwell stress tensor (SI).

            σ_ij = ε0 (E_i E_j - ½ δ_ij E²) + (1/μ0) (B_i B_j - ½ δ_ij B²)

        Parameters
        ----------
        E, B : arrays of shape (..., 3)

        Returns
        -------
        sigma : array of shape (..., 3, 3)
        """
        E = np.asarray(E, dtype=float)
        B = np.asarray(B, dtype=float)
        assert E.shape[-1] == 3 and B.shape[-1] == 3

        E2 = np.sum(E * E, axis=-1)
        B2 = np.sum(B * B, axis=-1)

        # Outer products
        EE = E[..., :, None] * E[..., None, :]
        BB = B[..., :, None] * B[..., None, :]

        eye = np.eye(3)
        sigma = EPS0 * (EE - 0.5 * E2[..., None, None] * eye)
        sigma += (1.0 / MU0) * (BB - 0.5 * B2[..., None, None] * eye)
        return sigma

    # ------------------------------------------------------------------
    def informational_stress(
        self,
        info_field: np.ndarray,
        n: int = 3,
    ) -> np.ndarray:
        """
        Construct a simple isotropic informational stress contribution.

        info_field : (...,) or (..., 3) — scalar LDOS proxy or vector
        Returns stress of shape (..., 3, 3)
        """
        w = self.W(n) * self.chi_vac
        info_field = np.asarray(info_field, dtype=float)

        if info_field.shape[-1:] == (3,):
            # vector → dyadic
            amp = info_field
            dyad = amp[..., :, None] * amp[..., None, :]
            trace = np.trace(dyad, axis1=-2, axis2=-1)
            eye = np.eye(3)
            return w * (dyad - 0.5 * trace[..., None, None] * eye)
        else:
            # scalar → isotropic pressure-like term
            eye = np.eye(3)
            return w * info_field[..., None, None] * eye

    # ------------------------------------------------------------------
    def surface_force(
        self,
        stress: np.ndarray,
        normals: np.ndarray,
        areas: np.ndarray,
    ) -> np.ndarray:
        """
        Integrate stress over a closed surface.

            F_i = ∫ σ_ij n_j dA

        Parameters
        ----------
        stress  : (N, 3, 3)
        normals : (N, 3)  — outward unit normals
        areas   : (N,)    — facet areas

        Returns
        -------
        F : (3,)
        """
        # traction = σ · n
        traction = np.einsum("...ij,...j->...i", stress, normals)
        return np.sum(traction * areas[:, None], axis=0)

    # ------------------------------------------------------------------
    def evaluate(
        self,
        E: np.ndarray,
        B: np.ndarray,
        normals: np.ndarray,
        areas: np.ndarray,
        info_field: Optional[np.ndarray] = None,
        n: int = 3,
    ) -> Dict[str, Any]:
        """
        Full evaluation on a discrete closed surface.

        Returns a dictionary containing:
          - F_em          : force from Maxwell stress alone
          - F_info        : force from informational term alone
          - F_total       : sum
          - W_used        : the numerical factor applied
          - model         : "star" or "M2"
          - null_test_ok  : True if zero fields produce zero force
        """
        E = np.asarray(E, dtype=float)
        B = np.asarray(B, dtype=float)
        normals = np.asarray(normals, dtype=float)
        areas = np.asarray(areas, dtype=float)

        # Maxwell part
        sigma_em = self.maxwell_stress_tensor(E, B)
        F_em = self.surface_force(sigma_em, normals, areas)

        # Informational part
        if info_field is None:
            F_info = np.zeros(3)
            sigma_info = None
        else:
            sigma_info = self.informational_stress(info_field, n=n)
            # broadcast if scalar field was given per-facet
            if sigma_info.ndim == 2:
                sigma_info = np.broadcast_to(
                    sigma_info, (len(areas), 3, 3)
                ).copy()
            F_info = self.surface_force(sigma_info, normals, areas)

        F_total = F_em + F_info

        # Null test
        null_ok = np.allclose(F_em, 0.0) if np.allclose(E, 0.0) and np.allclose(B, 0.0) else True

        return {
            "F_em": F_em,
            "F_info": F_info,
            "F_total": F_total,
            "W_used": self.W(n),
            "model": self.model,
            "null_test_ok": bool(null_ok),
            "warning": (
                "M2 exploratory — stability bound tension unresolved"
                if self.model == "M2"
                else None
            ),
        }


# ---------------------------------------------------------------------------
# Convenience: synthetic closed surface for unit tests
# ---------------------------------------------------------------------------
def make_unit_sphere_surface(n_theta: int = 16, n_phi: int = 32) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Return (centroids, normals, areas) for a unit sphere discretised
    in spherical coordinates. Useful for analytic checks.
    """
    theta = np.linspace(0, np.pi, n_theta + 1)
    phi = np.linspace(0, 2 * np.pi, n_phi + 1)
    dtheta = theta[1] - theta[0]
    dphi = phi[1] - phi[0]

    centroids = []
    normals = []
    areas = []
    for i in range(n_theta):
        for j in range(n_phi):
            th = 0.5 * (theta[i] + theta[i + 1])
            ph = 0.5 * (phi[j] + phi[j + 1])
            x = np.sin(th) * np.cos(ph)
            y = np.sin(th) * np.sin(ph)
            z = np.cos(th)
            centroids.append([x, y, z])
            normals.append([x, y, z])  # unit sphere
            areas.append(np.sin(th) * dtheta * dphi)
    return (
        np.array(centroids),
        np.array(normals),
        np.array(areas),
    )


def _self_test() -> None:
    """Basic sanity checks — run with python physics_evaluator.py"""
    print("Running self-tests …")
    ev = MaxwellStressTensorEvaluator(model="star")

    # 1. Null test
    cents, norms, areas = make_unit_sphere_surface(8, 16)
    E0 = np.zeros_like(cents)
    B0 = np.zeros_like(cents)
    out = ev.evaluate(E0, B0, norms, areas)
    assert np.allclose(out["F_total"], 0.0), "Null test failed"
    print("  null test passed")

    # 2. Uniform E field on sphere → net force must vanish (closed surface)
    E = np.zeros_like(cents)
    E[:, 0] = 1.0  # Ex = 1
    B = np.zeros_like(cents)
    out = ev.evaluate(E, B, norms, areas)
    assert np.allclose(out["F_em"], 0.0, atol=1e-10), "Uniform-E net force not zero"
    print("  uniform-E closed-surface test passed")

    # 3. W_star value
    assert abs(ev.W() - 0.08) < 1e-15
    print("  W_star lock passed")

    print("All self-tests passed.")


if __name__ == "__main__":
    _self_test()
