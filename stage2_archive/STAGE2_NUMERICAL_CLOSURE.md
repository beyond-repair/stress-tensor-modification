# Stage-2 Numerical Closure — Archive

**Date:** 2026-08-27  
**Repositories:** stress-tensor-modification, coherence-drive  
**Claim flags:** all remain **false**

---

## 1. Scope completed

| Study | Domain / constitutive choice | Continuum behaviour of |G| |
|-------|------------------------------|-----------------------------------------------------|
| Surface Realization A | Geometric scalar proxy (level sets follow mesh asymmetry) | Stable O(1); directionally stable |
| Surface Realization B | Electrostatic potential from collocation BEM (C6-style) | Machine-epsilon floor (consistent with zero) |
| Volume interior Yukawa | (-∇² + μ²)Ψ = 1, Ψ = 0 on ∂Ω, solid tet | **Decreases under refinement** → consistent with vanishing continuum limit |

No constant (κ, W, μ, source amplitude) was adjusted to the design target 3×10⁻⁸ N/W.

---

## 2. Primary negative result (interior volume)

On the solid tetrahedron with homogeneous Dirichlet and neutral source:

- |G| ∼ 10⁻⁵ at 512 tets, falling to ∼ 4×10⁻⁶ at 4096 tets.
- Successive relative changes remain large and the magnitude trends downward.
- **Verdict:** the interior Dirichlet signal vanishes in the continuum limit for this BVP.

The artificial O(1) geometric surface proxy (Realization A) is **not** a solution of a volume field equation and is therefore not a physical prediction of G.

---

## 3. Artifacts in this archive

| File | Role |
|------|------|
| `stage2_G_evaluation.py` | Surface proxy driver (Realizations A & B) + Richardson |
| `stage2_G_report.json` / `.md` | Surface study output |
| `volume_psi_solver.py` | Concrete P₁ Yukawa solver (solid tet, pure NumPy/SciPy) |
| `volume_psi_report.json` / `.md` | Interior volume μ-sweep |
| `richardson_extrapolation.py` | Shared Richardson utilities |
| `EXTERIOR_BVP_FORMULATION.md` | Exterior / transmission BVP specification (next gate) |
| `STAGE2_NUMERICAL_CLOSURE.md` | This document |

---

## 4. Claim flags (immutable in this archive)

```
experimental_validation     = false
thrust_validated            = false
energy_extraction_validated = false
target_fitting_performed    = false
mu_fitted_to_thrust         = false
mesh_convergence_established = false   # interior path shows vanishing G
```

---

## 5. Next legitimate numerical gate

Pivot to an **exterior or transmission** formulation for Ψ_info (see `EXTERIOR_BVP_FORMULATION.md`):

- Homogeneous Yukawa in the exterior with decay at infinity.
- Non-force-encoding hull BCs (Neumann homogeneous, constant Dirichlet, or Robin with fixed coefficient).
- Control geometry (sphere) must yield G → 0.
- Hull refinement + truncation-radius refinement required before any continuum claim.

Until an exterior study produces a mesh-converged, independently constrained, non-zero G under the rules above, the suite still does not possess a validated residual-force prediction.

---

*Stage 1 mathematics remains FROZEN. This archive records Stage-2 numerical evidence only.*
