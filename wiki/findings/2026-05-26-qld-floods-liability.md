---
type: finding
name: 2026-05-26-qld-floods-liability
description: QLD floods 2022 central CM liability USD 0.38B (AUD 10B × FAR=10.1%); Saudi Aramco USD 19M; global-share apportionment, GEV shift-fit PR
tags: [liability, floods, queensland, carbon-majors, far, damages]
related: [findings/2026-05-26-qld-floods-pr-era5, findings/2026-05-26-qld-floods-regional-amplification, findings/2026-05-18-black-summer-liability, disasters/qld-floods-2022, 2026-06-13-methodology-revision, 2026-06-17-lei-dropna-fix]
status: active
confidence: medium
last_updated: 2026-06-17
notebook: notebooks/03-liability/02_qld_floods_liability.ipynb
---

# 2022 SE QLD Floods — Liability

> **Revised 2026-06-13** ([[2026-06-13-methodology-revision]]). Apportionment now uses each entity's
> **global** warming share (not the Carbon Majors subtotal), and PR is the multiplicative GEV
> shift-fit. Central CM liability USD 0.73B → USD 0.31B; Saudi Aramco USD 62M → **USD 27M**.
>
> **Data fix 2026-06-17** ([[2026-06-17-lei-dropna-fix]]). Collective coverage corrected 44.6% →
> 75.5% after restoring ~562 GtCO₂e of dropped null-LEI emitters; the restored entities (Former
> Soviet Union, China Coal, Chevron) now top the ranking.
>
> **Denominator fix 2026-06-24** ([[2026-06-24-literature-cross-check]]). Warming-share denominator
> moved to **total anthropogenic CO₂ (FFI + AFOLU)**: collective coverage 75.5% → **53.6%**, matching
> Stuart-Smith et al. 2025 (~54%). Central CM liability USD 0.53B → **USD 0.38B**; Saudi Aramco USD
> 27M → **USD 19M**. The numbers below reflect this latest fix.

## Key Results

| Scenario | Damages | FAR [5–95%] | Total CM liability | Saudi Aramco |
|----------|---------|-------------|--------------------|-------------|
| Conservative (ICA insured) | AUD 5.56B / USD 3.89B | 0.101 [0.05–0.23] | USD 0.21B | USD 11M |
| **Central (direct economic, placeholder)** | **AUD 10B / USD 7.00B** | **0.101 [0.05–0.23]** | **USD 0.38B** | **USD 19M** [10–43] |
| Comprehensive (social, placeholder) | AUD 20B / USD 14.0B | 0.101 [0.05–0.23] | USD 0.76B | USD 38M |

The same primary FAR is applied to each damage scenario; uncertainty is from the PR bootstrap.
Carbon Majors cover ~54% of total anthropogenic CO₂ (FFI + AFOLU), so these are that fraction of climate-attributed damages.

## Attribution Chain

```
entity_liability = global_warming_share × FAR × total_damages
```

- **FAR = 0.101** from the multiplicative GEV shift-fit, primary β = ln(1.07)·α_QLD with α_QLD = 0.289
  (ERA5-observed wet-season Tmax) — see [[2026-05-26-qld-floods-pr-era5]]
- **Damages**: AUD 10B central (placeholder — verify against QLD Treasury / Deloitte / NEMA)

## Top 5 Entities (Central Scenario, USD M)

| Entity | Type | Liability [5–95%] | Global share |
|--------|------|-------------------|--------------|
| Former Soviet Union (1900–1991) | Nation State | 39.4 [20.0–90.0] | 5.58% |
| China (Coal, 1945–2004) | Nation State | 30.6 [15.5–69.8] | 4.33% |
| Saudi Aramco | State-owned | 19.0 [9.8–43.3] | 2.69% |
| Chevron | Investor-owned | 17.5 [8.9–40.0] | 2.49% |
| ExxonMobil | Investor-owned | 16.0 [8.1–36.4] | 2.26% |

Entity ranking and global shares are identical to Black Summer — warming shares are event-independent.

## EM-DAT Validation

EM-DAT 2022 AUS flood records: **REDACTED-DISNO (February)** records a redacted value (likely QLD + NSW),
in the right order of magnitude for the AUD 10B central placeholder. The ICA insured figure
(AUD 5.56B ≈ USD 3.9B) is the more defensible authoritative anchor.

## Key Caveats

1. **PR ≈ 1.11 is a conservative lower bound** ([[2026-05-26-qld-floods-pr-era5]]). The CMIP6 α_QLD
   sensitivity (0.882) gives PR ≈ 1.39 (FAR ≈ 0.28), roughly tripling the central liability to
   ~USD 1.04B. SST-based amplification would land between.
2. **Central and comprehensive damages are placeholders** (AUD 10B / 20B) — verify before use.
3. **Comparison to Black Summer**: central USD 0.38B vs USD 2.78B. Lower because FAR ≈ 0.10 vs 0.75
   — precipitation attribution via C-C scaling on a weak wet-season Tmax trend yields a much
   smaller signal than direct temperature attribution.

## Sensitivity (Central Damages AUD 10B)

| PR | FAR | Total CM Liability |
|----|-----|-------------------|
| 1.11 (primary) | 0.10 | USD 0.38B |
| 1.39 (CMIP6 α) | 0.28 | USD 1.04B |
| 2.0 | 0.50 | USD 1.88B |
| 4.0 | 0.75 | USD 2.82B |

## Outputs

- `data/processed/qld_floods_liability.parquet` — per-entity liability with PR-uncertainty columns
- `data/processed/qld_floods_scenario_totals.csv`
- `outputs/figures/qld_floods_sensitivity_aramco.png`
