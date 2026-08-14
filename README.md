# Stress Tensor Modification (Coherence Drive)

**© 2026 William B. Ware / Atomic Dream Labs — All Rights Reserved.**

**Status (2026-08-14):** Functional evaluator under locked \(W_\star=0.08\) (Option A). Coupling script to the 0.45 Sierpinski mesh is provided. Synthetic fields only — no propulsion performance claims.

---

## 1. Modified Stress Tensor

\[
T_{\rm eff}^{ij} = T_{\rm EM}^{ij} + W\cdot\chi_{\rm vac}\cdot(\text{informational contribution})
\]

- \(T_{\rm EM}^{ij}\): classical Maxwell stress (SI).
- Informational term: supplied by the caller (scalar LDOS proxy or vector field).
- Under **Option A**, \(W=W_\star=0.08\) is constant for the gravitational / force sector.

---

## 2. Evaluator

```bash
python physics_evaluator.py                # self-tests
python couple_sierpinski_evaluator.py      # mesh coupling demo
```

```python
from physics_evaluator import MaxwellStressTensorEvaluator, make_unit_sphere_surface

ev = MaxwellStressTensorEvaluator(model="star")   # locked W = 0.08
cents, norms, areas = make_unit_sphere_surface()
result = ev.evaluate(E, B, norms, areas, info_field=info)
```

Self-tests confirm null result, closed-surface cancellation for uniform E, and W lock.

---

## 3. Mesh Coupling

`couple_sierpinski_evaluator.py` imports the asymmetric tetrahedron from
`sierpinski-geometry-045`, builds surface elements, and evaluates residual
force under synthetic fields. Directional stability under aft-face refinement
is reported. No physical thrust number is claimed.

---

## 4. Guardrails

- Default model is `"star"` (constant \(W_\star=0.08\)).
- Model `"M2"` emits a `RuntimeWarning`.
- The evaluator never invents an LDOS or thrust number.

---

## Cross-References

- Geometry: [sierpinski-geometry-045](https://github.com/beyond-repair/sierpinski-geometry-045)
- Canonical mathematics (Option A locked): [ware-constant-phenomenology](https://github.com/beyond-repair/ware-constant-phenomenology)
- Consistency ledger: [CFTv3.3-IQG-Unified-Framework](https://github.com/beyond-repair/CFTv3.3-IQG-Unified-Framework)
