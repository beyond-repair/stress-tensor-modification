# Stress Tensor Modification (Coherence Drive)

**Status (2026-08-14):** Full-wave EFIE BEM (radiating Helmholtz kernel) + quasi-static / magnetostatic predecessors. Option A lock. No propulsion claims.

## Components

| File | Role |
|------|------|
| `physics_evaluator.py` | Maxwell stress + Ware term |
| `bem_sierpinski.py` | Electrostatic BEM |
| `rf_bem_sierpinski.py` | Magnetostatic + quasi-static RF |
| `fullwave_bem.py` | **Full-wave EFIE** with radiating Green's function |
| `couple_sierpinski_evaluator.py` | Synthetic-field coupling demo |

```bash
python physics_evaluator.py
python fullwave_bem.py
```

## Limits

Piecewise-constant face unknowns; PEC surface only; dense solver. Not a higher-order RWG / MLFMA production code.

## Cross-References

- Geometry: sierpinski-geometry-045
- Phenomenology: ware-constant-phenomenology
- Ledger: CFTv3.3-IQG-Unified-Framework
