# Volume Yukawa/Proca Evaluation of G

Generated: 2026-08-27T06:21:59.362682+00:00

volume_refine = 3
μ values      = [0.0, 1.0, 5.0]

## Results

| μ | tets | surface faces | |G| | dir | ψ_max |
|--:|-----:|--------------:|----:|-----|------:|
| 0.0 | 512 | 256 | 1.658363e-05 | (-0.004,0.944,-0.330) | 1.064163e-02 |
| 1.0 | 512 | 256 | 1.648494e-05 | (-0.002,0.944,-0.330) | 1.057224e-02 |
| 5.0 | 512 | 256 | 1.443417e-05 | (0.045,0.941,-0.337) | 9.118566e-03 |

## Claim flags

```
{
  "experimental_validation": false,
  "thrust_validated": false,
  "energy_extraction_validated": false,
  "target_fitting_performed": false,
  "mu_fitted_to_thrust": false
}
```

## Notes

- Domain is the solid base tetrahedron (filled).
- Sierpinski gasket is a surface-only construction; volume PDE uses the filled tet so that a well-posed interior BVP exists.
- μ is never optimised against a force target.
- chi_scale=1 exposes geometric shape of G; κ and W remain symbolic.

## Refinement study (μ = 1.0)

| refine | tets | faces | |G| | relative change |
|-------:|-----:|------:|----:|----------------:|
| 2 | 64 | 64 | 9.25e-05 | — |
| 3 | 512 | 256 | 1.65e-05 | 0.82 |
| 4 | 4096 | 1024 | 4.46e-06 | 0.73 |

|G| decreases under refinement → consistent with vanishing continuum limit.
