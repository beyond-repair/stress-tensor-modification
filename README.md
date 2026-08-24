<div align="center">

# Stress Tensor Modification

### The **working evaluators** for EM + Ware-style surface terms on 0.45 geometry

[![RESEARCH](https://img.shields.io/badge/research--grade-f59e0b?style=for-the-badge)](https://github.com/beyond-repair/ADL-Governance)
[![Claim](https://img.shields.io/badge/not_a_thrust_demo-7c3aed?style=for-the-badge)](https://github.com/beyond-repair/coherence-drive)

</div>

---

## Why this exists

Theory PDFs don’t push meshes.  
This repo is the **code path** that builds effective stress contributions and surface integrals so Stage-2 work has somewhere real to run — without pretending the output is certified thrust.

## Why you need it

| Role | Why open this |
|------|----------------|
| Numerics engineer | BEM / evaluator scripts on Sierpinski-type meshes |
| Auditor | See limits: piecewise BEM, not engineering-converged force |
| Theorist | Connect \(T_{\rm eff}\) talk to actual integrals |

**You need it for computation.** You do **not** need it as proof of propulsion.

## How it works

1. Take geometry from [sierpinski-geometry-045](https://github.com/beyond-repair/sierpinski-geometry-045) (or local mesh).  
2. Run electrostatic / magnetostatic / full-wave BEM modules as appropriate.  
3. Form surface contributions with Ware-weight hooks under **Option A** (M2 geometric only).  
4. Read residuals as **research-grade diagnostics**, not product specs.

| File | Role |
|------|------|
| `physics_evaluator.py` | Maxwell + Ware surface-force evaluator |
| `bem_sierpinski.py` | Electrostatic BEM |
| `rf_bem_sierpinski.py` | Magnetostatic / quasi-static RF |
| `fullwave_bem.py` | Full-wave EFIE |
| `couple_sierpinski_evaluator.py` | Mesh → evaluator demo |

```bash
python physics_evaluator.py
python bem_sierpinski.py
python fullwave_bem.py
```

**Baseline:** \(W_\star = 1/(4\pi)\) for phenomenology ledger; recursive \(W(n)\) per [MATH_THEORY_CLOSURE](https://github.com/beyond-repair/coherence-drive/blob/main/docs/MATH_THEORY_CLOSURE.md).

## Limits

Piecewise-constant BEM · PEC assumptions · dense solvers · directional trends may appear under refinement · **force magnitudes are not engineering-converged** · **no thrust claim**.

## Related

[ware-constant-phenomenology](https://github.com/beyond-repair/ware-constant-phenomenology) · [coherence-drive](https://github.com/beyond-repair/coherence-drive) · [CFTv3.3-IQG](https://github.com/beyond-repair/CFTv3.3-IQG-Unified-Framework)
