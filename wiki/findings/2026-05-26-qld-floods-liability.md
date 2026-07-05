---
type: finding
name: 2026-05-26-qld-floods-liability
description: QLD floods 2022 central CM liability USD 0.29B (AUD 7.7B Deloitte × FAR=10.1%); Saudi Aramco USD 14.6M; global-share apportionment, GEV shift-fit PR
tags: [liability, floods, queensland, carbon-majors, far, damages]
related: [findings/2026-05-26-qld-floods-pr-era5, findings/2026-05-26-qld-floods-regional-amplification, findings/2026-05-18-black-summer-liability, disasters/qld-floods-2022, 2026-06-13-methodology-revision, 2026-06-17-lei-dropna-fix, 2026-07-05-qld-damage-verification]
status: active
confidence: medium
last_updated: 2026-07-05
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
> Stuart-Smith et al. 2025 (~54%). Central CM liability USD 0.53B → USD 0.38B; Saudi Aramco USD
> 27M → USD 19M.
>
> **Damage verification 2026-07-05** ([[2026-07-05-qld-damage-verification]]). The AUD 10B "central"
> was an unsourced placeholder. Replaced with the **Deloitte Access Economics AUD 7.7B total-cost
> estimate** commissioned by the QLD Government (June 2022, QLD-scope). Central CM liability USD
> 0.38B → **USD 0.29B**; Saudi Aramco USD 19M → **USD 14.6M**. The unsourced AUD 20B comprehensive
> scenario was retired. The numbers below reflect this latest change.

## Key Results

| Scenario | Damages | FAR [5–95%] | Total CM liability | Saudi Aramco |
|----------|---------|-------------|--------------------|-------------|
| Conservative (ICA insured, final, QLD+NSW) | AUD 5.81B / USD 4.07B | 0.101 [0.05–0.23] | USD 0.22B | USD 11.0M |
| **Central (Deloitte total cost, QLD)** | **AUD 7.7B / USD 5.39B** | **0.101 [0.05–0.23]** | **USD 0.29B** | **USD 14.6M** [7.5–33] |

The same primary FAR is applied to each damage scenario; uncertainty is from the PR bootstrap.
Carbon Majors cover ~54% of total anthropogenic CO₂ (FFI + AFOLU), so these are that fraction of
climate-attributed damages. **Scope note**: the conservative insured figure is QLD+NSW while the
Deloitte total is QLD-only; insured < total holds (QLD is the bulk of the event), but the scopes
differ — see [[2026-07-05-qld-damage-verification]].

## Attribution Chain

```
entity_liability = global_warming_share × FAR × total_damages
```

- **FAR = 0.101** from the multiplicative GEV shift-fit, primary β = ln(1.07)·α_QLD with α_QLD = 0.289
  (ERA5-observed wet-season Tmax) — see [[2026-05-26-qld-floods-pr-era5]]
- **Damages**: AUD 7.7B central (Deloitte total cost, QLD govt-commissioned, verified 2026-07-05 —
  see [[2026-07-05-qld-damage-verification]])

## Top 5 Entities (Central Scenario AUD 7.7B, USD M)

| Entity | Type | Liability [5–95%] | Global share |
|--------|------|-------------------|--------------|
| Former Soviet Union (1900–1991) | Nation State | 30.3 [15.6–69.2] | 5.58% |
| China (Coal, 1945–2004) | Nation State | 23.5 [12.1–53.7] | 4.33% |
| Saudi Aramco | State-owned | 14.6 [7.5–33.4] | 2.69% |
| Chevron | Investor-owned | 13.5 [7.0–30.8] | 2.49% |
| ExxonMobil | Investor-owned | 12.3 [6.3–28.1] | 2.26% |

Entity ranking and global shares are identical to Black Summer — warming shares are event-independent.

## EM-DAT Validation

EM-DAT holds a February 2022 AUS flood record of the right order of magnitude, but its record-level
values are not reproduced here (EM-DAT Data Use Agreement — see [[datasets/emdat]]). EM-DAT is an
internal cross-check only and cannot be surfaced in the public app; the primary anchor is the
independently-sourced Deloitte AUD 7.7B (QLD total cost).

## Key Caveats

1. **PR ≈ 1.11 is a conservative lower bound** ([[2026-05-26-qld-floods-pr-era5]]). The CMIP6 α_QLD
   sensitivity (0.882) gives PR ≈ 1.39 (FAR ≈ 0.28), roughly tripling the central liability to
   ~USD 0.80B. SST-based amplification would land between.
2. **Damage scope mismatch**: conservative insured (AUD 5.81B) is QLD+NSW; central Deloitte total
   (AUD 7.7B) is QLD-only. Documented in [[2026-07-05-qld-damage-verification]].
3. **Comparison to Black Summer**: central USD 0.29B vs USD 2.78B. Lower because FAR ≈ 0.10 vs 0.75
   — precipitation attribution via C-C scaling on a weak wet-season Tmax trend yields a much
   smaller signal than direct temperature attribution.

## Sensitivity (Central Damages AUD 7.7B)

| PR | FAR | Total CM Liability |
|----|-----|-------------------|
| 1.11 (primary) | 0.10 | USD 0.29B |
| 1.39 (CMIP6 α) | 0.28 | USD 0.80B |
| 2.0 | 0.50 | USD 1.44B |
| 4.0 | 0.75 | USD 2.17B |

## Outputs

- `data/processed/qld_floods_liability.parquet` — per-entity liability with PR-uncertainty columns
- `data/processed/qld_floods_scenario_totals.csv`
- `outputs/figures/qld_floods_sensitivity_aramco.png`
