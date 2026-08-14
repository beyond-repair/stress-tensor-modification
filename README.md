# Stress Tensor Modification

**Status (2026-08-14):** Research-grade solvers. \(W_\star=1/(4\pi)\) default in phenomenology; evaluator defaults to model="star" with W=0.08 (0.5% difference — acceptable).

## Solvers

| File | Regime | Notes |
|------|--------|-------|
| physics_evaluator.py | Maxwell + Ware | Self-tests pass |
| bem_sierpinski.py | Electrostatic BEM | Direction stable under refinement |
| rf_bem_sierpinski.py | Magnetostatic + quasi-static RF | Thin-shell / Leontovich |
| fullwave_bem.py | Full-wave EFIE | Radiating Helmholtz kernel; piecewise-constant; PEC |

## Mesh Convergence

Directional unit-vector dots under aft-face refinement (n_aft=1→2→3) are O(0.99) for electrostatic/RF modes. Force *magnitudes* are not yet mesh-converged to engineering tolerance; piecewise-constant basis limits accuracy. RWG/higher-order remains open.

## Topological Pinch

No solver output confirms the 92% aft-face claim. Treat as hypothesis.

## Cross-Ref

phenomenology · sierpinski-geometry-045 · coherence-drive
