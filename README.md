<div align="center">

[![Lifecycle](https://img.shields.io/badge/●_RESEARCH-a855f7?style=for-the-badge&labelColor=0f0f23)](https://github.com/beyond-repair/ADL-Governance)
[![Claim](https://img.shields.io/badge/Claim_≤1-22c55e?style=for-the-badge&labelColor=0f0f23)](https://github.com/beyond-repair/ADL-Governance/blob/main/docs/CLAIM_VALIDATION.md)
[![Governance](https://img.shields.io/badge/ADL--Governance-7c3aed?style=for-the-badge&labelColor=0f0f23)](https://github.com/beyond-repair/ADL-Governance)

```
LIFECYCLE   RESEARCH
CLAIM       ≤1
NOT CLAIMED thrust · energy extraction · AGI · production autonomy
```

</div>

---

<div align="center">

# Stress Tensor Modification

### Research-grade **surface evaluators** on 0.45 geometry

[![RESEARCH](https://img.shields.io/badge/not_thrust_demo-7c3aed?style=for-the-badge)](https://github.com/beyond-repair/coherence-drive)
[![Claims](https://img.shields.io/badge/claim_flags-false-critical?style=for-the-badge)](CLAIM_STATUS.md)

</div>

---

## What this is

Executable **Maxwell stress + BEM** tools on the shared 0.45 asymmetric Sierpinski mesh.  
Bridges theory to surface integrals **without** certifying laboratory thrust.

See [CLAIM_STATUS.md](CLAIM_STATUS.md).

---

## Visual workflow

```text
 1. GEOMETRY     sierpinski-geometry-045 → mesh / STL
        │
 2. FIELD PATH   bem_sierpinski · rf_bem · fullwave_bem
        │
 3. STRESS       physics_evaluator (Maxwell + optional Ware-weight hooks)
        │
 4. SURFACE      ∮ T · dA   (diagnostics)
        │
 5. REPORT       residuals / directionality / estimated pattern A
                 — NOT product F/P, NOT reactionless thrust
```

| Step | How | Why |
|-----:|-----|-----|
| 1 | Shared 0.45 mesh | One shape language |
| 2 | BEM / EFIE modules | Fields on real geometry |
| 3 | Maxwell + optional Ware hooks | Engineering weight ≠ silent cosmology rescale |
| 4 | Surface integral | Momentum-closure story becomes numeric-capable |
| 5 | Research limits | No engineering-converged thrust claim |

```bash
python physics_evaluator.py          # Maxwell null + uniform-E sphere tests
python bem_sierpinski.py             # electrostatic BVP; net F residual is discretization
python fullwave_bem.py               # radiating EFIE; diagnostic F + estimated |A|
python couple_sierpinski_evaluator.py  # synthetic fields demo (not physical BVP)
```

---

## Maxwell stress (implemented)

$$
T_{ij}
=
\varepsilon_0\big(E_i E_j-\tfrac12\delta_{ij}E^2\big)
+
\mu_0^{-1}\big(B_i B_j-\tfrac12\delta_{ij}B^2\big)
$$

`physics_evaluator.py` integrates \(F_i=\int T_{ij}n_j\,dA\) and passes null / closed-surface checks.

---

## Known gaps (honest)

| Gap | Status |
|-----|--------|
| Dual-surface Class B \(\epsilon_F=\|F_d+F_X\|\) | **Not implemented** |
| Full far-field Maxwell momentum flux | **Estimated** pattern \(A\) only in `fullwave_bem` |
| Stage-2 continuum Yukawa/Proca nulls | On branch `stage2-numerical-closure` |
| Laboratory validation | **false** |

---

## Conjunction

Index: [coherence-drive](https://github.com/beyond-repair/coherence-drive)  
Geometry: [sierpinski-geometry-045](https://github.com/beyond-repair/sierpinski-geometry-045)  
Class B protocol: coherence-drive `docs/CLASS_B_VERIFICATION_PROTOCOL.md`


---

<div align="center">

**REWRITE · BUILD · TRANSCEND**

Governing source: [ADL-Governance](https://github.com/beyond-repair/ADL-Governance) · [Claim levels 0–5](https://github.com/beyond-repair/ADL-Governance/blob/main/docs/CLAIM_VALIDATION.md)

</div>
