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

No configuration file. The 0.45 gasket is generated in-tree by `local_geometry.py` (a frozen face subdivision). Nothing is downloaded at runtime. `sierpinski-geometry-045` is not imported.

```bash
git clone https://github.com/beyond-repair/stress-tensor-modification.git
cd stress-tensor-modification
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install -e .
stress-tensor-modification
python physics_evaluator.py
python bem_sierpinski.py
python rf_bem_sierpinski.py
python fullwave_bem.py
python couple_sierpinski_evaluator.py
pytest -q
```

`stress-tensor-modification` is the same report as `python cli.py`.

| Command | What it prints | What it does not say |
|---------|----------------|----------------------|
| `stress-tensor-modification` | Star anchor, M2 W(n), sphere null, open-gasket BEM residual, pattern \|A\|/c | Thrust, closed epsilon_F, or a fitted constant |
| `pytest -q` | Those checks plus the sphere integrator | A laboratory result |

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
| Dual-surface Class B \(\epsilon_F=\|F_d+F_X\|\) | **Not implemented.** `closure.py` only checks uniform-E on two spheres. |
| Full far-field Maxwell momentum flux | **Estimated** pattern \(A\) only in `fullwave_bem` |
| Closed-conductor null on this mesh | **Miss.** The gasket is not watertight. Electrostatic \|F\| grew from about 3.0e-11 to 8.2e-8 as `n_aft` went from 1 to 3. |
| Star anchor vs M2 pin | **Not the same number.** `W_star = 1/(4π) ≈ 0.079577`. M2 `W(3)=0.08` is a separate pin. `W(5)≈0.126726` is above the model-internal 0.125 bound. Not refit. |
| Engineering target 3e-8 N/W | **Miss.** Photon ceiling 1/c ≈ 3.336e-9 N/W is already below the target (~9/c). Largest printed |A|/c on the default grid is about 1.22e-9 N/W. |
| Stage-2 continuum Yukawa/Proca nulls | On branch `stage2-numerical-closure` (not this default-branch repair) |
| Laboratory validation | **false** |

Notes in `docs/` that quote a scout \|A\|~0.002–0.003 or a closed epsilon_F are historical. The commands above are the numbers this tree prints. Magnetostatic \|Fm\| at `B_inf=1` T is \(10^{6}\)–\(10^{10}\) because the open-mesh \(B^2/(2\mu_0)\) integral does not cancel. That is not a device force.

`physics_evaluator_snippet.py` raises `ImportError` on import. It is a quarantined placeholder, not an entry point.

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
