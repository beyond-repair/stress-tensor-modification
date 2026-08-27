# Stage-2 Numerical Closure Archive

**Status: FINAL for tested BVPs (scalar + Proca P-E2)**  
**Claim flags: all false**

## Final verdict

Neither scalar Yukawa paths nor Proca P-E2 (nodal scout) support a robust non-vanishing continuum G. Tet residuals track at or below spherical noise floors under joint refinement.

See [STAGE2_FINAL_CLOSURE.md](STAGE2_FINAL_CLOSURE.md).

## Key artifacts

| File | Role |
|------|------|
| STAGE2_FINAL_CLOSURE.md | Executive closure (scalar + Proca) |
| proca_paired_floor_report.md | Proca sphere vs tet null |
| proca_sphere_control_report.md | Proca spherical noise floor |
| exterior_v2_paired_convergence.* | Scalar exterior null |
| volume_psi_report.* | Interior Yukawa null |
| stage2_G_report.* | Surface proxies A/B |
| EXTERIOR_BVP_FORMULATION.md | Exterior BVP specification |

Nédélec for Proca P-E2: halted (low information gain for this BVP).

No parameter was fitted to 3×10⁻⁸ N/W. Stage 1 freeze unchanged.
