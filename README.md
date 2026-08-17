# Stress Tensor Modification

**Status (2026-08-17):** Research-grade solvers. Not a propulsion demonstration.

**Baseline:** \(W_\star = 1/(4\pi)\approx 0.08\) (phenomenology ledger). Option A: M2 is geometric/LDOS enhancement only.

## Active modules

| File | Role |
|------|------|
| `physics_evaluator.py` | Maxwell + Ware surface-force evaluator |
| `bem_sierpinski.py` | Electrostatic BEM on 0.45 Sierpinski |
| `rf_bem_sierpinski.py` | Magnetostatic + quasi-static RF |
| `fullwave_bem.py` | Full-wave EFIE (radiating Helmholtz kernel) |
| `couple_sierpinski_evaluator.py` | Mesh → evaluator integration demo |

## Deprecated

| File | Note |
|------|------|
| `physics_evaluator_snippet.py` | **Deprecated.** Raises on import. Historical zero-Maxwell / M2 fragment. |

```bash
python physics_evaluator.py
python bem_sierpinski.py
python fullwave_bem.py
```

Geometry dependency: sibling repo `sierpinski-geometry-045`.

## Limits

Piecewise-constant BEM unknowns; PEC surface; dense solvers. Directional stability under refinement is observed; force magnitudes are not engineering-converged. No thrust claim.

## Cross-references

- Math ledger: [ware-constant-phenomenology](https://github.com/beyond-repair/ware-constant-phenomenology)
- Consistency: [CFTv3.3-IQG-Unified-Framework](https://github.com/beyond-repair/CFTv3.3-IQG-Unified-Framework)
- Geometry: [sierpinski-geometry-045](https://github.com/beyond-repair/sierpinski-geometry-045)
