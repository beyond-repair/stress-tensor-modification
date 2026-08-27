# Exterior v2 Paired Convergence

Generated: 2026-08-27T06:55:51.598259+00:00
μ=1.0  BC=E2  n_radial=4

| R | n_ang | sphere |G| | tet |G| | ratio |
|--:|------:|------------:|--------:|------:|
| 3.0 | 30 | 6.9481e-02 | 2.6121e-02 | 0.38 |
| 3.0 | 50 | 5.8550e-02 | 1.6596e-02 | 0.28 |
| 5.0 | 30 | 2.8287e-02 | 9.2751e-03 | 0.33 |
| 5.0 | 50 | 2.3947e-02 | 3.6225e-03 | 0.15 |
| 8.0 | 30 | 1.3055e-02 | 4.4991e-03 | 0.34 |
| 8.0 | 50 | 9.1612e-03 | 7.8479e-04 | 0.09 |

## Claim flags

```
{
  "experimental_validation": false,
  "thrust_validated": false,
  "energy_extraction_validated": false,
  "target_fitting_performed": false,
  "mu_fitted_to_thrust": false,
  "alpha_fitted_to_thrust": false,
  "R_outer_fitted_to_thrust": false
}
```

## Interpretation

- Sphere |G| is the numerical noise floor for this discretisation.
- Tet |G| is only meaningful if it remains well above the sphere floor under simultaneous increase of R_outer and n_ang.
- If tet |G| tracks the sphere floor downward, the residual is consistent with zero.
- Claim flags remain false regardless of the numerical ratio.

**Verdict:** Tet residual tracks below the sphere floor → consistent with vanishing continuum G for exterior E2 Yukawa.
