# Stress Tensor Modification (Coherence Drive)

**Status (2026-08-14):** Evaluator + electrostatic / magnetostatic / quasi-static RF BEM on the Sierpinski surface. Option A lock. No propulsion claims.

## Components

| File | Role |
|------|------|
| `physics_evaluator.py` | Maxwell stress + Ware term |
| `bem_sierpinski.py` | Electrostatic BEM |
| `rf_bem_sierpinski.py` | Magnetostatic + quasi-static RF promotion |
| `couple_sierpinski_evaluator.py` | Synthetic-field coupling demo |

```bash
python physics_evaluator.py
python bem_sierpinski.py
python rf_bem_sierpinski.py
```

## Limits

Quasi-static / thin-shell idealisations. Full-wave radiation boundary conditions and volumetric dielectrics remain open.

## Cross-References

- Geometry: sierpinski-geometry-045
- Phenomenology: ware-constant-phenomenology
- Ledger: CFTv3.3-IQG-Unified-Framework
