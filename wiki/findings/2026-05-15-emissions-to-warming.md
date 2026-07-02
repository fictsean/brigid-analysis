---
type: finding
name: 2026-05-15-emissions-to-warming
tags: [fair, warming-attribution, carbon-majors, uncertainty]
related: [carbon-majors-database, emissions-to-forcing, far-probability-ratio, 2026-05-15-carbon-majors-ingest]
status: active
confidence: medium
last_updated: 2026-06-17
notebook: notebooks/02-attribution/01_emissions_to_warming.ipynb
---

# Emissions → Warming Attribution — Initial Results

Proportional warming contributions for all 178 Carbon Majors entities, using FaIR v2.2 with the fair-calibrate v1.4 posterior ensemble (841 configs, constrained against IPCC AR6 observations).

> **Updated 2026-06-24** ([[2026-06-24-literature-cross-check]]). The warming-share **denominator**
> was changed from fossil-CO₂-only to **total anthropogenic CO₂ (FFI + AFOLU)**: the previous version
> divided fossil CO₂ by a fossil-only base and applied it to *total* all-forcing warming, over-stating
> the collective share at ~76% vs the peer-reviewed ~54% (Stuart-Smith et al. 2025). Collective share
> is now 53.6%. Per-entity magnitudes were already right (Aramco ~0.03–0.04°C ≈ Nature 2025). An
> earlier 2026-06-17 update ([[2026-06-17-lei-dropna-fix]]) had fixed a separate data-loss bug
> (restoring null-LEI emitters); the numbers below reflect both fixes.

## Key Numbers

| Metric | Value |
|--------|-------|
| Total anthropogenic warming by 2020 (FaIR median) | **1.18 °C** [0.87–1.57] vs 1850–1900 |
| Carbon Majors collective share of total anthropogenic CO2 (FFI+AFOLU) | **53.6%** |
| Carbon Majors collective attributed warming | **0.63 °C** [0.47–0.84] (~54% of total) |

Peer-reviewed benchmark: Stuart-Smith et al. 2025 (*Nature*) ≈ 54% (0.7°C of 1.3°C to 2023);
Ekwurzel et al. 2017 ≈ 42–50% of GMST rise. (NB: the ~71% Heede figure is a share of *emissions*,
not warming — not a valid anchor for this number.)

## Top 5 Entity Warming Contributions (as of 2020)

| Entity | Type | m°C median [5–95th] |
|--------|------|---------------------|
| Former Soviet Union (1900–1991) | Nation State | 65.9 [48.5–87.6] |
| China (Coal, 1945–2004) | Nation State | 51.1 [37.7–68.0] |
| Saudi Aramco | State-owned | 31.7 [23.4–42.2] |
| Chevron | Investor-owned | 29.3 [21.6–39.1] |
| ExxonMobil | Investor-owned | 26.7 [19.7–35.5] |

## Scope Sensitivity

Scope 3 (product combustion) dominates — for the top entity (Former Soviet Union):
- **S1 + S3 total**: 65.9 m°C
- **S3 only**: 57.8 m°C (88%)
- **S1 only**: 8.0 m°C (12%)

This is legally significant: if liability frameworks exclude scope 3, attributed warming shrinks ~8×.

## Methodology Notes

- **Proportional attribution**: entity_warming = (entity cumulative CO2e / global cumulative *total* anthropogenic CO2) × FaIR ΔT
- **Global denominator**: RCMIP CO2 FFI + CO2 AFOLU historical emissions (total anthropogenic CO₂), cumulative 1750–2020
- **Uncertainty source**: FaIR ensemble spread — captures ECS/TCR uncertainty (not emissions uncertainty)
- **Baseline**: 1850–1900 pre-industrial mean (IPCC AR6 convention)
- **Validation**: FaIR median gives 1.04°C for 2011–2020 vs IPCC AR6 best estimate of 1.07°C ✓

## Caveats

- Coverage: Carbon Majors covers ~71% of global fossil CO2 (Heede, an *emissions* share) but only ~54% of total anthropogenic CO2 (FFI+AFOLU) — the latter is the warming-share basis used here and matches Stuart-Smith et al. 2025 (~54%). A fully CO₂e-consistent denominator (non-CO₂ forcers) is the remaining refinement
- CH4 treated as CO2e via GWP100; shorter-lived gases would require pulse-response weighting for exact attribution
- Proportionality assumption (TCRE linearity) is well-supported for CO2 but approximate for multi-gas totals
- Uncertainty ranges reflect climate model uncertainty only; emissions data uncertainty not yet propagated

## Outputs

- `data/processed/entity_warming_contribution.parquet` — 178 rows; median + 5/95th percentile warming contribution per entity
- `data/processed/fair_global_temperature.parquet` — FaIR ensemble temperature timeseries (1750–2021)

## Next Steps

- Ingest EM-DAT disaster records to pair warming contributions with additional events (requires registration)
- ✅ Applied to Black Summer 2019–20 — see [[2026-05-18-black-summer-liability]]
- ✅ Regional amplification applied — see [[2026-05-23-australia-regional-amplification]]
