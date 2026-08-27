# Stage-2 Numerical Closure Archive

**Status: FINAL for tested BVPs**  
**Claim flags: all false**

## Final verdict

Neither the interior Dirichlet Yukawa BVP nor the exterior E2 Yukawa BVP supports a robust non-vanishing physical G in the continuum limit under the tested constitutive proxies.

See [STAGE2_FINAL_CLOSURE.md](STAGE2_FINAL_CLOSURE.md).

## Key artifacts

| File | Role |
|------|------|
| STAGE2_FINAL_CLOSURE.md | Executive closure statement |
| exterior_v2_paired_convergence.md / .json | Sphere floor vs tet residual |
| volume_psi_report.* | Interior Yukawa null result |
| stage2_G_report.* | Surface proxies A/B |
| EXTERIOR_BVP_FORMULATION.md | Exterior BVP specification |
| STAGE2_NUMERICAL_CLOSURE.md | Intermediate closure note |
| richardson_extrapolation.py | Shared Richardson utilities |

Executable solvers (`exterior_psi_solver_v2.py`, `volume_psi_solver.py`, `stage2_G_evaluation.py`) live in the working tree and regenerate the reports above.

No parameter was fitted to 3×10⁻⁸ N/W. Stage 1 freeze is unchanged.
