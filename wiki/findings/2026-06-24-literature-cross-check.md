---
type: finding
tags: [literature, validation, cross-check, carbon-majors, attribution, methodology]
related: [stuart-smith-2025, ekwurzel-2017, wwa-studies, emissions-to-forcing, attribution-chain, 2026-06-17-lei-dropna-fix, 2026-06-13-methodology-revision]
status: settled
confidence: high
last_updated: 2026-06-24
---

# Literature cross-check + warming-share denominator fix

Systematic cross-check of every quantitative finding against the published literature, plus the
methodology fix and the validation harness it motivated. Headline outcome: most results check out, but our **collective Carbon Majors warming share was overstated (~76% → corrected ~54%)**, and two literature anchors in the wiki were wrong.

## Validation harness (the durable guardrail)

To stop this class of drift (the LEI-dropna bug, this denominator bug) recurring, the key values are now **pinned** in `tests/validation_benchmarks.json` (each with a citation/DOI) and checked by `scripts/validate_pipeline.py` (`src/attribution/validation.py`). Categories: **literature** (external anchors), **internal** (conservation/coherence), **golden** (frozen headline outputs). `scripts/build_notebooks.py` now runs the harness after every rebuild. Running it against the *pre-fix* outputs flagged exactly the two collective-warming benchmarks as FAIL while everything else passed — proving it catches the drift.

## Inconsistency 1 (HIGH, fixed) — collective warming share overstated

- **Was**: 75.5% of fossil CO₂ → 0.89°C / 1.18°C ≈ **76%** of warming.
- **Literature**: Stuart-Smith et al. 2025 (*Nature*) **~54%** (0.7°C of 1.3°C); Ekwurzel et al. 2017
  **~42–50%** of GMST rise.
- **Root cause**: `01_emissions_to_warming` divided Carbon-Majors **fossil** CO₂ by a **fossil-only**
  denominator (RCMIP CO₂ FFI, ~1719 Gt) and multiplied by **total all-forcing** warming (1.18°C).
  Carbon Majors don't cause the land-use-CO₂ / non-CO₂ forcing, so the fossil-CO₂ share over-states
  their share of *total* warming.
- **Fix (2026-06-24)**: denominator → **total anthropogenic CO₂ = CO₂ FFI + CO₂ AFOLU** (both in the
  same FaIR/RCMIP run). Collective share **53.6%**, attributed warming **0.63°C [0.47–0.84]** — in
  line with Nature 2025. A fully CO₂e-consistent denominator (non-CO₂ forcers) remains a follow-up.
- **Per-entity was already right**: Saudi Aramco 0.045°C → 0.032°C, both ≈ Nature 2025's ~0.04°C.
  The drift was purely in the collective denominator, not the per-entity scale.

### Headline impact (liability scales with `global_share`)
| Quantity | Before fix | After fix |
|----------|-----------|-----------|
| Collective CM coverage | 75.5% | **53.6%** |
| Collective attributed warming | 0.89°C | **0.63°C** [0.47–0.84] |
| Black Summer central liability | USD 3.92B | **USD 2.78B** [2.18–3.46] |
| QLD floods central liability | USD 0.53B | **USD 0.38B** [later USD 0.29B — see note] |
| Saudi Aramco (Black Summer central) | USD 197M | **USD 139M** [109–173] |

> **Note (2026-07-05)**: the QLD central USD 0.38B here was computed at the then-placeholder AUD 10B
> damage figure. That figure was later verified and replaced with the Deloitte AUD 7.7B total-cost
> estimate, giving USD 0.29B. This does not affect the denominator fix documented on this page (a
> pure `global_share` change); it is a separate damage-input correction. See
> [[2026-07-05-qld-damage-verification]].

## Inconsistency 2 (MEDIUM, fixed) — "Heede ~71%" mis-used to validate the warming share

~71% (Heede / InfluenceMap) is a share of **emissions**, not warming. Pages claiming "75.5% ≈ ~71% (so our warming share is validated)" conflated the two; the relevant *warming*-attribution literature is ~50–54%. Corrected wherever it appeared (`emissions-to-warming`, `emissions-to-forcing`, `ekwurzel-2017`, `attribution-chain`, `CLAUDE.md`).

## Inconsistency 3 (MEDIUM, fixed) — Ekwurzel per-entity anchor wrong by ~10×

The wiki cited "Saudi Aramco ~0.37°C (Ekwurzel)". Ekwurzel reports no robust single-company figure; the value is off by ~10× (per-entity contributions are tens of m°C). Corrected to **~0.04°C** (our 0.032°C; Nature 2025 ~0.04°C). "~0.5°C for 90 producers" → **~0.4°C** (42–50% of ~0.9°C GMST rise).

## Inconsistency 4 (LOW, clarified) — WWA metric precision

Our Black Summer PR=4.0 matches WWA's **ERA5 FWI7x-SM result (">4")**, not the model-based FWI ("≥30%"). Both appear in van Oldenborgh et al. 2021; the wiki now names the exact metric, and notes the MSR (">9") and heat (~10× obs / ≥2× models) context. The comparison stays valid; only labeling.

## Confirmed consistent (no change)

| Finding | Ours | Literature | Verdict |
|---------|------|-----------|---------|
| Black Summer PR / FAR | 4.0 / 0.752 | WWA ERA5 FWI7x-SM ">4" (10.5194/nhess-21-941-2021) | ✓ |
| FaIR warming 2011–2020 | 1.06°C | IPCC AR6 ~1.07°C | ✓ |
| Carbon Majors total emissions | 1,435.6 GtCO₂e (to 2024) | InfluenceMap (~1,421 to 2022, unverified) | ✓ within ~1% |
| Per-entity Aramco | 0.032°C | Nature 2025 ~0.04°C | ✓ |
| QLD 2022 floods | PR=1.11 (sole estimate) | No published PR study (confirmed) | ✓ |

## QLD 2022: newer literature (qualitative)

No probabilistic attribution (PR) study exists for the Feb–Mar 2022 SE QLD floods, so our PR=1.11 remains the sole quantitative estimate. But 2025 papers now characterise the event — *How February 2022 redefines extreme floods in Australia* (Comm. Earth & Env., s43247-025-02307-z) and *A Multiscale Evaluation of the Wet 2022 in Eastern Australia* (J. Climate, JCLI-D-24-0224.1) — both emphasising La Niña + warm SST drivers, consistent with our conservative framing.

## Sources

- Stuart-Smith et al. 2025, *Nature*, doi:10.1038/s41586-025-09450-9 — see [[stuart-smith-2025]].
- van Oldenborgh et al. 2021, NHESS 21:941, doi:10.5194/nhess-21-941-2021.
- Ekwurzel et al. 2017, *Climatic Change* 144:579, doi:10.1007/s10584-017-1978-0 — see [[ekwurzel-2017]].
- IPCC AR6 WG1 SPM (human-induced warming ~1.07°C, 2010–2019).
