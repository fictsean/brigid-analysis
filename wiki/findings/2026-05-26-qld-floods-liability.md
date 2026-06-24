---
type: finding
name: 2026-05-26-qld-floods-liability
description: QLD floods 2022 central CM liability USD 0.53B (AUD 10B × FAR=10.1%); Saudi Aramco USD 27M; global-share apportionment, GEV shift-fit PR
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
> **75.5%** after restoring ~562 GtCO₂e of dropped null-LEI emitters. Central CM liability USD 0.31B
> → **USD 0.53B**. Saudi Aramco is unchanged (incumbent); the rise comes from restored entities
> (Former Soviet Union, China Coal, Chevron), which now top the ranking.

## Key Results

| Scenario | Damages | FAR [5–95%] | Total CM liability | Saudi Aramco |
|----------|---------|-------------|--------------------|-------------|
| Conservative (ICA insured) | AUD 5.56B / USD 3.89B | 0.101 [0.05–0.23] | USD 0.30B | USD 15M |
| **Central (direct economic, placeholder)** | **AUD 10B / USD 7.00B** | **0.101 [0.05–0.23]** | **USD 0.53B** | **USD 27M** [13–61] |
| Comprehensive (social, placeholder) | AUD 20B / USD 14.0B | 0.101 [0.05–0.23] | USD 1.06B | USD 53M |

The same primary FAR is applied to each damage scenario; uncertainty is from the PR bootstrap.
Carbon Majors cover ~75% of global fossil CO₂, so these are that fraction of climate-attributed damages.

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
| Former Soviet Union (1900–1991) | Nation State | 55.4 [28.1–126.6] | 7.86% |
| China (Coal, 1945–2004) | Nation State | 43.0 [21.8–98.3] | 6.10% |
| Saudi Aramco | State-owned | 26.7 [13.5–61.0] | 3.79% |
| Chevron | Investor-owned | 24.7 [12.5–56.4] | 3.50% |
| ExxonMobil | Investor-owned | 22.5 [11.4–51.3] | 3.19% |

Entity ranking and global shares are identical to Black Summer — warming shares are event-independent.

## EM-DAT Validation

EM-DAT 2022 AUS flood records: **REDACTED-DISNO (February)** records a redacted value (likely QLD + NSW),
in the right order of magnitude for the AUD 10B central placeholder. The ICA insured figure
(AUD 5.56B ≈ USD 3.9B) is the more defensible authoritative anchor.

## Key Caveats

1. **PR ≈ 1.11 is a conservative lower bound** ([[2026-05-26-qld-floods-pr-era5]]). The CMIP6 α_QLD
   sensitivity (0.882) gives PR ≈ 1.39 (FAR ≈ 0.28), roughly tripling the central liability to
   ~USD 1.48B. SST-based amplification would land between.
2. **Central and comprehensive damages are placeholders** (AUD 10B / 20B) — verify before use.
3. **Comparison to Black Summer**: central USD 0.53B vs USD 3.92B. Lower because FAR ≈ 0.10 vs 0.75
   — precipitation attribution via C-C scaling on a weak wet-season Tmax trend yields a much
   smaller signal than direct temperature attribution.

## Sensitivity (Central Damages AUD 10B)

| PR | FAR | Total CM Liability |
|----|-----|-------------------|
| 1.11 (primary) | 0.10 | USD 0.53B |
| 1.39 (CMIP6 α) | 0.28 | USD 1.48B |
| 2.0 | 0.50 | USD 2.64B |
| 4.0 | 0.75 | USD 3.96B |

## Outputs

- `data/processed/qld_floods_liability.parquet` — per-entity liability with PR-uncertainty columns
- `data/processed/qld_floods_scenario_totals.csv`
- `outputs/figures/qld_floods_sensitivity_aramco.png`
