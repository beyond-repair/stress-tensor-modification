# BEM / Dual-Surface ε_F Exploration

**Date:** 2026-08-31  
**Flags:** `epsilon_F_magnitude_closed=false`, `thrust_validated=false`

---

## 1. Definition (physics-compatible)

$$
\mathbf{F}_d = -\oint_{\partial\Omega} \langle T^{ij}\rangle n_j\,dA
\qquad
\mathbf{F}_X = \oint_{S_R} \langle T^{ij}\rangle n_j\,dA
$$

$$
\epsilon_F = \frac{\|\mathbf{F}_d+\mathbf{F}_X\|}{|\mathbf{F}_X|+\delta}
$$

**Same** stress tensor, **same** units, both surfaces. Pass: $\epsilon_F\to 0$ under mesh + $R$ refinement for a pure radiating solution.

For EM (SI Maxwell):

$$
T_{ij}=\varepsilon_0\Big(E_iE_j-\tfrac12\delta_{ij}E^2\Big)
+\mu_0^{-1}\Big(B_iB_j-\tfrac12\delta_{ij}B^2\Big)
$$

cycle-averaged for time-harmonic fields.

---

## 2. What exists in this repo

| Module | Provides | Missing for ε_F |
|--------|----------|------------------|
| `fullwave_bem.py` | Dense EFIE, face currents $I$, pattern $\mathcal{A}$ estimate | Far + near Maxwell $E,B$ → dual $T$ |
| `physics_evaluator.py` | $T_{\rm EM}$ + surface $\oint$ | Only **one** surface; needs $S_R$ samples |
| Pattern $A$ in fullwave | Class B direction proxy | Not $\epsilon_F$ magnitude |

README already: dual-surface $\epsilon_F$ **not implemented**.

---

## 3. Scout calculation (scalar single-layer dual surface)

Same $\langle T\rangle$ from complex $\nabla\psi$ on hull exterior points and far sphere. Aft-biased face weights on 0.45 mesh.

| n_aft | R | $\|F_d\|$ | $\|F_X\|$ | $\epsilon_F$ |
|------:|--:|----------:|----------:|-------------:|
| 1 | 5–40 | ~13 | $10^{-4}$–$5\times10^{-4}$ | $O(10^4)$–$O(10^5)$ |
| 2 | 5–40 | ~9.3 | similar | $O(10^4)$–$O(10^5)$ |
| 3 | 5–40 | ~7.2 | similar | $O(10^4)$–$O(10^5)$ |

**Interpretation:** magnitudes **not closed**. Near-surface $F_d$ is dominated by **singular self-field / near-zone stress**, not matched to radiated momentum flux $F_X$. Alignment $F_d$ vs $-F_X$ is unstable. This is a **numerical bookkeeping failure**, not a reactionless discovery.

---

## 4. Why ε_F blows up (and how BEM fixes the path)

1. **Self-field on the hull** — evaluating $\nabla\psi$ a tiny offset outside piecewise-constant sources still sees huge local gradients; radiation stress is a small remainder.
2. **No RWG / principal-value treatment** — production BEM uses careful singularity subtraction for on-surface fields.
3. **Scalar proxy ≠ Maxwell** — full $\epsilon_F$ needs $E,B$ from EFIE currents (or equivalent), then Maxwell $T$ on both surfaces.
4. **Normalization** — optional: report $\epsilon_F$ only after subtracting reactive near-field or using **momentum form from far-field only** for $F_X$ and **induced power-consistent** device force.

Practical Class B path used in literature:

- $F_X \propto (P_{\rm rad}/c)\,\mathcal{A}$ from far pattern (already in `fullwave_bem`)
- $F_d$ from full near-field Maxwell integral **or** set $F_d:=-F_X$ by conservation and only **validate** pattern + $P_{\rm rad}$

True dual-surface Maxwell $\epsilon_F$ requires higher-fidelity field recovery.

---

## 5. Implementation roadmap (to actually close ε_F)

1. From `fullwave_bem` currents $I_f$, reconstruct **E, B** in exterior via radiation integrals (not only scalar $\psi$).
2. Sample on offset hull facets + far sphere $S_R$.
3. Build cycle-avg Maxwell $T$ with `MaxwellStressTensorEvaluator`.
4. Integrate both; compute $\epsilon_F(R,n_{\rm aft},f)$.
5. Refine mesh / $R$ / angular density; require $\epsilon_F$ decreasing.
6. Sphere control: $\|\mathcal{A}\|\to0$, $\epsilon_F$ still defined if $F_X\to0$ carefully.

Until then: **do not** set `epsilon_F_magnitude_closed=true`.

---

## 6. Relation to Coherence Drive claims

| Claim | Status |
|-------|--------|
| Dual-surface conservation check | **Explored; not closed** |
| Reactionless residual | **Not supported** (huge $\epsilon_F$ is error, not thrust) |
| Pattern $\mathcal{A}$ estimate | Available in fullwave |
| Lab thrust | false |

See also: coherence-drive `docs/EPSILON_F_DUAL_SURFACE_DESIGN.md`, `PHYSICS_COMPATIBLE_CLOSURE.md`.
