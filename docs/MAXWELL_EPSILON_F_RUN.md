# Maxwell dual-surface ε_F run (EFIE path)

**Date:** 2026-08-31  
**Flags:** epsilon_F_magnitude_closed=false; thrust_validated=false

## Method

1. `fullwave`-style dense EFIE → face currents I on 0.45 mesh  
2. Reconstruct exterior E (radiation integral proxy)  
3. B ≈ r̂×E/c (far); crude near B  
4. Cycle-avg Maxwell T on hull offset + far sphere  
5. ε_F = ||F_d+F_X|| / (|F_X|+δ)

Also report |A| and F/P ≤ |A|/c from pattern.

## Results (scout)

| n_aft | f | R | ε_F (near–far T) | |A| | F/P from A |
|------:|--:|--:|-----------------:|----:|-----------:|
| 1 | 100 MHz | 8–30 | ~4–6 | ~1.2e-3 | ~4e-12 |
| 1 | 300 MHz | 8–30 | ~8–9 | ~2.5–3e-3 | ~1e-11 |
| 2 | 100 MHz | 8–30 | ~19–23 | ~1.4–1.7e-2 | ~5e-11 |
| 2 | 300 MHz | 8–30 | **~0.63** | ~0.25 | ~8e-10 |

Best residual still O(1), not →0. One band looks less bad (~0.63) but is **not** closed under refinement claims.

## Class B construction

Setting F_d := −(P_rad/c) A gives ε_F=0 **by definition**. That is conservation bookkeeping, not a dual-surface proof.

Photon F/P from A remains ≪ 3e-8 target.

## Conclusion

- Dual-surface Maxwell ε_F **explored** on this stack  
- **Not closed** (need RWG, better near fields, mesh study)  
- No reactionless claim  
- Compatible path remains F_d = −F_X with far-field A

See BEM_EPSILON_F_EXPLORATION.md for roadmap.
