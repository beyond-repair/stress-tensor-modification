# Proca Paired Floor Report (sphere vs tet)

Generated: 2026-08-27T10:55:46.474707+00:00  
μ=1.0  λ=1.0  A_H=[0.0, 0.0, 1.0]  n_radial=3

| R | n_ang | sphere |G| | tet |G| | ratio |
|--:|------:|------------:|--------:|------:|
| 3.0 | 25 | 3.306527e-02 | 1.370158e-02 | 0.414 |
| 3.0 | 40 | 3.504265e-02 | 4.659606e-03 | 0.133 |
| 5.0 | 25 | 1.660231e-02 | 8.102656e-03 | 0.488 |
| 5.0 | 40 | 1.358097e-02 | 1.515071e-03 | 0.112 |
| 8.0 | 25 | 7.377210e-03 | 3.693653e-03 | 0.501 |
| 8.0 | 40 | 4.955676e-03 | 1.255439e-03 | 0.253 |

## Verdict

Tet residual remains at or below the spherical noise floor (ratio range 0.11–0.50) under the tested (R, n_ang) grid. Consistent with vanishing continuum G for Proca P-E2 under this discretisation; no continuum non-zero G established.

## Nédélec note

Upgrading to Nédélec edge elements would likely lower the absolute noise floor but is not expected to convert a sub-floor residual into a continuum signal for this BVP. Nédélec development for Proca P-E2 is **halted** unless a new, independently motivated BC or constitutive map is introduced.

## Claim flags

```
{
  "experimental_validation": false,
  "thrust_validated": false,
  "energy_extraction_validated": false,
  "target_fitting_performed": false,
  "mu_fitted_to_thrust": false,
  "lambda_fitted_to_thrust": false
}
```
