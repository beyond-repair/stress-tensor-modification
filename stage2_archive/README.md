# Stage-2 Numerical Closure Archive

This directory permanently records the Stage-2 numerical evaluation of the informational surface integral G on the Coherence Drive 0.45 geometry.

## Contents

| File | Description |
|------|-------------|
| [STAGE2_NUMERICAL_CLOSURE.md](STAGE2_NUMERICAL_CLOSURE.md) | Summary, negative result, claim flags |
| [EXTERIOR_BVP_FORMULATION.md](EXTERIOR_BVP_FORMULATION.md) | Exterior / transmission BVP specification (next gate) |
| [volume_psi_report.md](volume_psi_report.md) / [.json](volume_psi_report.json) | Interior Yukawa μ-sweep + refinement |
| [stage2_G_report.md](stage2_G_report.md) | Surface proxy Realizations A & B |
| [richardson_extrapolation.py](richardson_extrapolation.py) | Shared Richardson utilities |

Full executable solvers (`volume_psi_solver.py`, `stage2_G_evaluation.py`) are maintained in the working tree / sibling checkouts and produce the reports above when run against `sierpinski-geometry-045`.

## Primary result

**Interior Dirichlet Yukawa BVP:** |G| decreases under mesh refinement and is consistent with a **vanishing continuum limit**.

**Surface geometric proxy (Realization A):** O(1) stable integral — **not** a volume PDE solution; not a physical prediction.

**Surface electrostatic proxy (Realization B):** machine-epsilon floor.

## Claim flags (locked)

```
experimental_validation     = false
thrust_validated            = false
energy_extraction_validated = false
target_fitting_performed    = false
mu_fitted_to_thrust         = false
```

No parameter was fitted to 3×10⁻⁸ N/W.

## Next gate

Exterior or transmission BVP for Ψ_info — see EXTERIOR_BVP_FORMULATION.md.
