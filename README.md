# Stress Tensor Modification (Coherence Drive)

**© 2026 William B. Ware / Atomic Dream Labs — All Rights Reserved.**

**Status (2026-08-14):** Functional evaluator under locked \(W_\star = 0.08\). M2 mode available with explicit stability warning. No propulsion performance claims.

---

## 1. Modified Stress Tensor

\[
T_{\rm eff}^{ij} = T_{\rm EM}^{ij} + W\cdot\chi_{\rm vac}\cdot(\text{informational contribution})
\]

- \(T_{\rm EM}^{ij}\): classical Maxwell stress (SI).
- Informational term: supplied by the caller (scalar LDOS proxy or vector field).

---

## 2. Evaluator

```bash
python physics_evaluator.py          # runs self-tests
```

```python
from physics_evaluator import MaxwellStressTensorEvaluator, make_unit_sphere_surface

ev = MaxwellStressTensorEvaluator(model="star")   # locked W = 0.08
cents, norms, areas = make_unit_sphere_surface()
E = ...  # shape (N, 3)
B = ...  # shape (N, 3)
info = ...  # optional scalar or (N, 3)

result = ev.evaluate(E, B, norms, areas, info_field=info)
print(result["F_total"], result["W_used"])
```

Self-tests confirm:
- zero fields → zero force (null test),
- uniform E on a closed surface → net Maxwell force = 0,
- W is locked at 0.08 for model="star".

---

## 3. Guardrails

- Default model is `"star"` (constant \(W_\star = 0.08\)).
- Model `"M2"` emits a `RuntimeWarning` because tabulated values exceed the earlier ghost-free bound.
- The evaluator never invents an LDOS or thrust number; it only contracts fields you supply.

---

## Cross-References

- Geometry: [sierpinski-geometry-045](https://github.com/beyond-repair/sierpinski-geometry-045)
- Canonical mathematics: [ware-constant-phenomenology](https://github.com/beyond-repair/ware-constant-phenomenology)
- Consistency ledger: [CFTv3.3-IQG-Unified-Framework](https://github.com/beyond-repair/CFTv3.3-IQG-Unified-Framework)
