# Claim status — stress-tensor-modification

| Field | Value |
|-------|--------|
| Classification | RESEARCH |
| Experimental validation | **false** |
| Thrust validated | **false** |
| Reactionless closed thrust | **false** |
| Target fitting performed | **false** |
| epsilon_F (Class B dual-surface residual) | **not reported** |
| Maxwell stress implementation | present (`physics_evaluator.py`) |
| Stage-2 continuum null archive | branch `stage2-numerical-closure` |

GitHub description text that implies proven thrust is **out of date**; this file is authoritative.

## Runnable check (default branch)

`stress-tensor-modification` / `pytest` exercise the Maxwell evaluator, the open-gasket BEM toys, and the synthetic Ware-weight hook.

| Printed quantity | This tree | Not claimed |
|------------------|-----------|-------------|
| `W_star` | 0.07957747154594767 = 1/(4π) | the M2 pin 0.08 |
| M2 `W(5)` | 0.12672591879955855 | a stay under 0.125 |
| electrostatic \|F\| n_aft 1→3 | 2.991747e-11 → 8.229403e-08 | a closed-conductor null or thrust |
| max \|A\|/c on the default grid | 1.217031e-09 N/W | the 3e-8 N/W target |
| 1/c | 3.335641e-09 N/W | reaching 3e-8 N/W |
| epsilon_F | not computed | a closed residual |

Constants are not refit. No thrust, propulsion, or completed physical law is claimed.
