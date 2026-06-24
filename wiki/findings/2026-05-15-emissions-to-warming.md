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

> **Updated 2026-06-17** ([[2026-06-17-lei-dropna-fix]]). The collective share/warming and the
> entity rankings below were corrected after fixing a data-loss bug in `cm_entity_year.parquet` that
> had silently dropped ~562 GtCO₂e of null-LEI emitters (Former Soviet Union, China Coal, Chevron,
> NIOC…). Collective share 44.6% → **75.5%**; incumbents with valid LEIs (Aramco, ExxonMobil) are
> unchanged — the previously-missing emitters now appear at the top of the rankings.

## Key Numbers

| Metric | Value |
|--------|-------|
| Total anthropogenic warming by 2020 (FaIR median) | **1.18 °C** [0.87–1.57] vs 1850–1900 |
| Carbon Majors collective share of global fossil CO2 | **75.5%** |
| Carbon Majors collective attributed warming | **0.89 °C** [0.66–1.19] (~76% of total) |

## Top 5 Entity Warming Contributions (as of 2020)

| Entity | Type | m°C median [5–95th] |
|--------|------|---------------------|
| Former Soviet Union (1900–1991) | Nation State | 92.8 [68.4–123.5] |
| China (Coal, 1945–2004) | Nation State | 72.0 [53.1–95.9] |
| Saudi Aramco | State-owned | 44.7 [32.9–59.5] |
| Chevron | Investor-owned | 41.3 [30.5–55.0] |
| ExxonMobil | Investor-owned | 37.6 [27.7–50.1] |

## Scope Sensitivity

Scope 3 (product combustion) dominates — for the top entity (Former Soviet Union):
- **S1 + S3 total**: 92.8 m°C
- **S3 only**: 81.5 m°C (88%)
- **S1 only**: 11.3 m°C (12%)

This is legally significant: if liability frameworks exclude scope 3, attributed warming shrinks ~8–9×.

## Methodology Notes

- **Proportional attribution**: entity_warming = (entity cumulative CO2e / global cumulative fossil CO2) × FaIR ΔT
- **Global denominator**: RCMIP CO2 FFI historical emissions (consistent with Global Carbon Project), cumulative 1750–2020
- **Uncertainty source**: FaIR ensemble spread — captures ECS/TCR uncertainty (not emissions uncertainty)
- **Baseline**: 1850–1900 pre-industrial mean (IPCC AR6 convention)
- **Validation**: FaIR median gives 1.04°C for 2011–2020 vs IPCC AR6 best estimate of 1.07°C ✓

## Caveats

- Coverage: Carbon Majors covers ~75% of global fossil CO2, close to the often-cited ~71% Heede figure; the small excess over 71% comes from the CO₂e-numerator vs CO₂-FFI-denominator mismatch (tracked follow-up)
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
