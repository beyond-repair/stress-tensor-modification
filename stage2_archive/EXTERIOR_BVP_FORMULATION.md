# Exterior / Transmission BVP for Ψ_info — Formulation

**Status:** Design specification only. No exterior numerical solution is claimed.  
**Parent:** Stage-2 numerical closure (interior Yukawa null result archived).  
**Claim flags:** all false.

---

## 1. Motivation

The interior Dirichlet problem

    -∇²Ψ + μ²Ψ = 1    in Ω
    Ψ = 0              on ∂Ω

on the solid tetrahedron yields a surface integral G that **decreases under mesh refinement** and is consistent with a vanishing continuum limit. That negative result is archived and does not raise any claim level.

If the physical hypothesis places the informational field **outside** the craft (or as a transmission problem across the hull), an exterior or transmission formulation is the next legitimate numerical gate.

---

## 2. Exterior Yukawa problem (recommended first exterior path)

Let Ω be the solid tetrahedron (craft interior) and Ωᶜ = ℝ³ \ Ω̄ the exterior.

**Field equation (exterior):**

    -∇²Ψ + μ²Ψ = 0     in Ωᶜ

**Decay / radiation condition at infinity:**

    Ψ(r) = O( e^{-μ|r|} / |r| )    as |r| → ∞   (μ > 0)
    Ψ(r) = O( 1/|r| )              as |r| → ∞   (μ = 0)

**Boundary condition on the hull ∂Ω (non-force-encoding options):**

| Option | BC | Notes |
|--------|-----|-------|
| E1 Neumann homogeneous | ∂ₙΨ = 0 on ∂Ω | No preferred-direction data |
| E2 Dirichlet constant | Ψ = c (constant) on ∂Ω | Constant set to 1 by linearity; no angular structure injected |
| E3 Robin | ∂ₙΨ + αΨ = 0 | α > 0 fixed, not fitted to force |
| E4 Transmission | continuity of Ψ and normal flux | See §3 |

**Source:** none in the exterior (homogeneous). Any drive must come from boundary data or an interior source that does not encode a laboratory force direction beyond the geometry itself.

The surface integral G is still evaluated on ∂Ω from the exterior trace of ∇Ψ.

---

## 3. Transmission (interior–exterior) formulation

    -∇²Ψᵢ + μᵢ² Ψᵢ = fᵢ     in Ω
    -∇²Ψₑ + μₑ² Ψₑ = 0      in Ωᶜ
    Ψᵢ = Ψₑ                 on ∂Ω
    ∂ₙΨᵢ = ∂ₙΨₑ             on ∂Ω
    Ψₑ → 0                  at infinity

- fᵢ remains a neutral source (constant or zero-mean) if used; never tuned to thrust.
- μᵢ, μₑ are independent model parameters, reported, never fitted to force.
- Transmission conditions inject **no** preferred-direction bias beyond the geometry of ∂Ω.

---

## 4. Discretisation notes (exterior)

1. **Truncation:** replace Ωᶜ by a bounded exterior shell Ω_R with a Dirichlet-to-Neumann or Robin approximation of the Yukawa decay on the artificial boundary ∂B_R.
2. **Mesh:** tetrahedral mesh of the shell; hull faces must conform to the surface generator used in Stage-2.
3. **FEM:** same P₁ (or higher) assembly; artificial-boundary DOFs carry the approximate radiation operator.
4. **Gradient recovery:** element-wise or patch recovery on hull facets → σ_info → G.
5. **Null tests:**
   - μ → ∞ should force Ψ → 0 and G → 0.
   - Spherical hull (control geometry) should produce G → 0 by symmetry.
   - Refinement of both hull and truncation radius must be reported.

---

## 5. What is *not* permitted

- Boundary data or source terms chosen to maximise |G| or to match 3×10⁻⁸ N/W.
- Silent absorption of the design target into μ, α, or source amplitude.
- Elevation of thrust_validated or experimental_validation on the basis of an exterior residual alone.

---

## 6. Exit criteria for an exterior numerical study

1. Mesh-converged G (hull refinement + truncation-radius refinement).
2. Control geometry (sphere) yields |G| consistent with zero.
3. μ (and any Robin coefficient) reported and not optimised against force.
4. Claim flags remain false unless a separate, explicit claim-validation process is completed under ADL-Governance rules.

---

*Document status: formulation only. Implementation of the exterior solver is a subsequent Stage-2 task.*
