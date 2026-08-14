# Stress Tensor Modification (Coherence Drive)

**© 2026 William B. Ware / Atomic Dream Labs — All Rights Reserved.**

**Status (2026-08-14):** Evaluator + electrostatic BEM on the Sierpinski surface. Option A lock (\(W_\star=0.08\)). No propulsion performance claims.

---

## Components

| File | Role |
|------|------|
| `physics_evaluator.py` | Maxwell stress + Ware term; self-tests |
| `couple_sierpinski_evaluator.py` | Synthetic-field coupling demo |
| `bem_sierpinski.py` | **Real** electrostatic BEM on the asymmetric mesh |

```bash
python physics_evaluator.py
python bem_sierpinski.py          # requires sibling sierpinski-geometry-045
python couple_sierpinski_evaluator.py
```

---

## BEM Notes

- Integral-equation collocation for surface charge on a conductor in uniform E.
- Net force residual measures geometric asymmetry + discretisation (ideally zero for a closed conductor).
- Direction stabilises under aft-face refinement.
- Quasi-static only; full RF solution remains open.

---

## Cross-References

- Geometry: [sierpinski-geometry-045](https://github.com/beyond-repair/sierpinski-geometry-045)
- Phenomenology / SPARC report: [ware-constant-phenomenology](https://github.com/beyond-repair/ware-constant-phenomenology)
- Consistency ledger: [CFTv3.3-IQG-Unified-Framework](https://github.com/beyond-repair/CFTv3.3-IQG-Unified-Framework)
