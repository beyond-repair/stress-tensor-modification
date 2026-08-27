# Stage-2 Final Numerical Closure

**Date:** 2026-08-27  
**Repositories:** coherence-drive, stress-tensor-modification  
**Claim flags:** permanently **false** (no target fitting performed)

---

## 1. Executive statement

Under the constitutive proxies and boundary-value problems tested in Stage 2, **neither the interior Dirichlet Yukawa problem nor the exterior E2 Yukawa problem supports a robust, non-vanishing physical G in the continuum limit**.

The informational surface integral that would source a residual force via

    ΔF = W(n) χ_vac G

is consistent with **zero** once discretisation noise is controlled. Stage 1 mathematics remains FROZEN; no claim level is elevated.

---

## 2. Evidence summary

| Study | Constitutive / BVP | Continuum behaviour of |G| |
|-------|--------------------|------------------------------------------------------|
| Surface Realization A | Geometric scalar proxy (not a PDE solution) | Stable O(1) — **proxy only; not physical prediction** |
| Surface Realization B | Electrostatic potential (C6-style) | Machine-epsilon floor |
| Interior volume Yukawa | (−∇²+μ²)Ψ=1, Ψ=0 on ∂Ω | Decreases under refinement → **vanishing** |
| Exterior E2 Yukawa (v2) | Homogeneous Yukawa, Ψ=const on hull, monopole DtN at R_outer | Tet residual **tracks below spherical noise floor** and falls with R and angular density → **consistent with zero** |

### Exterior v2 paired floor (μ = 1, BC = E2)

| R | n_ang | sphere floor | tet residual | ratio |
|--:|------:|-------------:|-------------:|------:|
| 3.0 | 30 | 6.9×10⁻² | 2.6×10⁻² | 0.38 |
| 3.0 | 50 | 5.9×10⁻² | 1.7×10⁻² | 0.28 |
| 5.0 | 30 | 2.8×10⁻² | 9.3×10⁻³ | 0.33 |
| 5.0 | 50 | 2.4×10⁻² | 3.6×10⁻³ | 0.15 |
| 8.0 | 30 | 1.3×10⁻² | 4.5×10⁻³ | 0.34 |
| 8.0 | 50 | 9.2×10⁻³ | 7.8×10⁻⁴ | 0.09 |

Spherical E1 null test: |G|=0 exactly.

---

## 3. What was *not* done

- No adjustment of κ, W(n), μ, Robin α, source amplitude, or R_outer to match 3×10⁻⁸ N/W.
- No elevation of thrust_validated, experimental_validation, or energy_extraction_validated.
- No interpretation of geometric proxies or discretisation residuals as laboratory thrust.

---

## 4. Claim flags (locked)

```
experimental_validation     = false
thrust_validated            = false
energy_extraction_validated = false
target_fitting_performed    = false
mu_fitted_to_thrust         = false
alpha_fitted_to_thrust      = false
R_outer_fitted_to_thrust    = false
mesh_convergence_established = false   # residuals consistent with zero
```

---

## 5. Implications for the Coherence Drive programme

1. **Stage 2 numerical closure (tested BVPs):** complete with a **negative** result for non-zero continuum G.
2. **Stage 3 experiment** is not justified by the present numerical evidence under these constitutive choices.
3. Further numerical work is only warranted if a **new, independently motivated** constitutive map or BVP is introduced — and that work must again pass the spherical-control floor test without target fitting.
4. Stage 1 symbolic freeze is unchanged. The design target remains a design target, not a prediction.

---

## 6. Artifact index

| Artifact | Location |
|----------|----------|
| This document | stage2_archive/STAGE2_FINAL_CLOSURE.md |
| Exterior v2 paired convergence | exterior_v2_paired_convergence.json / .md |
| Interior volume reports | volume_psi_report.* |
| Surface proxy reports | stage2_G_report.* |
| Exterior BVP formulation | EXTERIOR_BVP_FORMULATION.md |

---

*Stage-2 numerical closure is final for the tested interior Dirichlet and exterior E2 Yukawa constitutive paths. All claim flags remain false.*
