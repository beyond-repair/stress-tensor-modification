<div align="center">

# Stress Tensor Modification

### Research-grade **surface evaluators** on 0.45 geometry

[![RESEARCH](https://img.shields.io/badge/not_thrust_demo-7c3aed?style=for-the-badge)](https://github.com/beyond-repair/coherence-drive)
[![Stage 2](https://img.shields.io/badge/Stage_2-mesh_tools-0ea5e9?style=for-the-badge)](MESH_CONVERGENCE.md)

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
 5. CONVERGENCE  mesh_convergence_study + Richardson extrapolation
        │
 6. REPORT       residuals / directionality — NOT product F/P
```

| Step | How | Why |
|-----:|-----|-----|
| 1 | Shared 0.45 mesh | One shape language |
| 2 | BEM / EFIE modules | Fields on real geometry |
| 3 | Ware hooks under Option A | Engineering weight ≠ silent W★ rescale |
| 4 | Surface integral | Momentum-closure story becomes numeric-capable |
| 5 | Richardson + depth sweep | Stage-2 mesh behaviour, not marketing |
| 6 | Research limits | No engineering-converged thrust claim |

```bash
python physics_evaluator.py
python bem_sierpinski.py
python fullwave_bem.py
python mesh_convergence_study.py   # Stage-2 driver (needs sibling geometry repo)
python richardson_extrapolation.py # self-test
```

---

## Stage-2 mesh tools (this branch)

| File | Role |
|------|------|
| [`richardson_extrapolation.py`](richardson_extrapolation.py) | Order estimation + continuum limit |
| [`mesh_convergence_study.py`](mesh_convergence_study.py) | BEM depth sweep → JSON/Markdown report |
| [`MESH_CONVERGENCE.md`](MESH_CONVERGENCE.md) | Protocol and interpretation rules |
| [`MLFMA_NOTES.md`](MLFMA_NOTES.md) | Hierarchical acceleration exploration (no production MLFMA yet) |

**Claim flags remain false.** A clean Richardson table does not raise `thrust_validated` or `experimental_validation`.

**Conjunction:** feeds Stage-2 path under [coherence-drive](https://github.com/beyond-repair/coherence-drive); phenomenology scoring stays in ware-constant-phenomenology.
