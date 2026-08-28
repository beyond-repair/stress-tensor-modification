# Stage-2 Numerical Evaluation of G

Generated: 2026-08-27T00:46:10.800582+00:00

## Constitutive realizations (independent, not tuned)

- **A**: geometric scalar proxy (level sets follow z-asymmetry only)
- **B**: electrostatic potential from collocation BEM (C6-style Ψ~φ)
- χ-scale (placeholder) = 1.0 (κ, W left symbolic)

## Per-depth results

| n_aft | faces | |G_A| | dir_A | |G_B| | dir_B | |F_Maxwell| |
|------:|------:|-----:|------|-----:|------|----------:|
| 1 | 12 | 1.080046e+00 | (-0.205,-0.955,0.214) | 1.186946e-24 | (0.000,1.000,-0.000) | 2.991747e-11 |
| 2 | 18 | 1.007341e+00 | (-0.279,-0.953,0.115) | 3.251825e-23 | (0.998,0.047,-0.047) | 1.671028e-09 |
| 3 | 36 | 1.069464e+00 | (-0.199,-0.965,0.170) | 8.891083e-21 | (0.393,-0.546,-0.740) | 8.229403e-08 |

## Richardson analysis — Realization A (geometric)

- magnitudes         : ['1.080046e+00', '1.007341e+00', '1.069464e+00']
- relative changes   : ['6.7316e-02', '6.1670e-02']
- observed orders    : [nan]
- p_used             : 1.0
- Q* (magnitude)     : 1.131586550525755
- |Q*|               : 1.1404647965246746
- direction dots     : [0.9924765915221672, 0.9953189577200389]

## Richardson analysis — Realization B (electrostatic proxy)

- magnitudes         : ['1.186946e-24', '3.251825e-23', '8.891083e-21']
- relative changes   : ['2.6397e+01', '2.7242e+02']
- observed orders    : [-8.143324556724668]
- p_used             : 1.0
- Q* (magnitude)     : 1.7749648586168764e-20
- |Q*|               : 1.7769157667328367e-20
- direction dots     : [0.04712582370300598, 0.4008254171180751]

## Claim flags

```
{
  "experimental_validation": false,
  "thrust_validated": false,
  "energy_extraction_validated": false,
  "mesh_convergence_established": false,
  "target_fitting_performed": false
}
```

## Interpretation

- Realization A: robust O(1) geometric integral (proxy only, not a volume PDE solution).
- Realization B: collapses to machine zero.
- No constant was adjusted to match 3e-8 N/W.
