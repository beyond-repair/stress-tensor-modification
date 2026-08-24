<div align="center">

# Stress Tensor Modification

### Research-grade **surface evaluators** on 0.45 geometry

[![RESEARCH](https://img.shields.io/badge/not_thrust_demo-7c3aed?style=for-the-badge)](https://github.com/beyond-repair/coherence-drive)

</div>

---

## Why unique

The only **executable** stress/BEM cluster in the Ware line — bridges theory talk to integrals without certifying thrust.

---

## Visual workflow

```text
 1. GEOMETRY     sierpinski-geometry-045 → mesh / STL
        │
 2. FIELD PATH   bem_sierpinski · rf_bem · fullwave_bem
        │
 3. STRESS       physics_evaluator (EM + Ware-weight hooks)
        │
 4. SURFACE      ∮ T_eff · dA   (diagnostics)
        │
 5. REPORT       residuals / directionality — NOT product F/P
```

| Step | How | Why |
|-----:|-----|-----|
| 1 | Shared 0.45 mesh | One shape language |
| 2 | BEM / EFIE modules | Fields on real geometry |
| 3 | Ware hooks under Option A | Engineering weight ≠ silent W★ rescale |
| 4 | Surface integral | Momentum-closure story becomes numeric-capable |
| 5 | Research limits | No engineering-converged thrust claim |

```bash
python physics_evaluator.py
python bem_sierpinski.py
python fullwave_bem.py
```

**Conjunction:** feeds Stage-2 path under [coherence-drive](https://github.com/beyond-repair/coherence-drive); phenomenology scoring stays in ware-constant-phenomenology.
