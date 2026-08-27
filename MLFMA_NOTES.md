# MLFMA Acceleration — Exploration Notes

**Status:** Design exploration only. **No production MLFMA implementation is present.**  
**Claim level:** 0 (infrastructure discussion).  
**Parent:** [coherence-drive](https://github.com/beyond-repair/coherence-drive) Stage-2 numerical closure.

---

## 1. Why MLFMA appears on the roadmap

Current BEM modules (`bem_sierpinski.py`, `fullwave_bem.py`, `rf_bem_sierpinski.py`) use dense collocation / EFIE matrices:

- Storage: O(N²)
- Factorisation / solve: O(N³) (direct) or O(N²) per matvec (iterative)

Face count on the asymmetric Sierpinski grows rapidly with `n_aft`. At depths ≥ 4 the dense path becomes memory- and time-prohibitive on commodity hardware. Hierarchical acceleration is the classical remedy for surface integral equations.

---

## 2. Algorithmic sketch (standard MLFMA)

1. **Octree / cluster tree** over surface centroids (or RWG edge mid-points if upgraded).
2. **Multipole expansion** of the Green’s function (Laplace for electrostatics; Helmholtz for full-wave) about cluster centres.
3. **Aggregation** (upward pass): child multipoles → parent multipoles.
4. **Translation** (well-separated clusters): multipole-to-local operators.
5. **Disaggregation** (downward pass): local expansions → field at observers.
6. **Near-field** correction: direct evaluation for adjacent clusters.

Complexity target: O(N log N) per matvec for low-frequency / low-order expansions; higher constants for broadband / high-order cases.

---

## 3. Integration points in the existing codebase

| Existing component | MLFMA touch-point |
|--------------------|-------------------|
| `mesh_elements()` | Supply centroids, areas, normals to tree builder |
| `bem_solve_conductor` / `efie_matrix` | Replace dense `G` / `Z` assembly + `np.linalg.solve` by iterative solver (GMRES) + MLFMA matvec |
| `physics_evaluator.surface_force` | Unchanged — still consumes traction on the same facets |
| `sierpinski_generator` | Unchanged — geometry remains the source of truth |

Recommended first step: keep piecewise-constant unknowns; replace only the dense matrix path. Upgrade to RWG basis only after the hierarchical kernel is validated on the electrostatic (Laplace) problem.

---

## 4. Implementation options (research ranking)

| Option | Effort | Risk | Notes |
|--------|--------|------|-------|
| Pure-Python educational MLFMA | Medium | High constant factors | Useful for verification; not production |
| Bind existing C++/Fortran MLFMA (e.g. via pybind) | High | Integration / licence | Fastest route to large-N |
| Low-rank / H-matrix approximation (ACA, HODLR) | Medium | Different theory | Often easier to prototype than full MLFMA |
| FMM for Laplace only (electrostatic path) | Lower | Limited to static | Matches current `bem_sierpinski` first |

Recommendation for Stage-2: prototype a **Laplace FMM / low-rank** matvec for the electrostatic residual study before attempting full-wave Helmholtz MLFMA.

---

## 5. Claim discipline

- Presence of an MLFMA prototype does **not** raise `thrust_validated` or `experimental_validation`.
- Accelerated residuals remain mesh-dependent until a documented convergence table (see `MESH_CONVERGENCE.md`) is reviewed.
- Any timing or memory claims must be accompanied by hardware and N figures; no silent extrapolation to “real-time propulsion simulation.”

---

## 6. Exit criteria for an MLFMA prototype (future)

1. Matvec residual vs dense reference < 1e-3 relative on a depth-3 mesh.
2. GMRES convergence to the same residual tolerance as the dense solver.
3. Memory scaling demonstrably better than O(N²) for N ≥ 5 000.
4. Results fed into the same Richardson / mesh-convergence pipeline without changing claim flags.

Until those criteria are met, the dense path remains the reference implementation.

---

## 7. References (classical)

- Rokhlin, Greengard — original FMM / MLFMA literature.
- Chew, Jin, Michielssen, Song — *Fast and Efficient Algorithms in Computational Electromagnetics*.
- Existing open-source starting points for later binding: scuff-em, bempp, Puma-EM, etc. (licence review required before any integration).

---

*Document status: exploration only. No executable MLFMA code is claimed by this file.*
