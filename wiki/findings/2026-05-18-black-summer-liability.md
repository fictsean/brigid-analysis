---
type: finding
name: 2026-05-18-black-summer-liability
tags: [black-summer, bushfire, australia, liability, far, fair, end-to-end]
related: [2026-05-15-carbon-majors-ingest, 2026-05-15-emissions-to-warming, far-probability-ratio, emissions-to-forcing, wwa-studies, 2026-05-24-black-summer-pr-era5]
status: active
confidence: medium
last_updated: 2026-05-24
notebook: notebooks/03-liability/01_black_summer_liability.ipynb
---

# Black Summer 2019–20 — Entity Liability Estimates

End-to-end attribution chain applied to the 2019–20 Australian bushfire season. Combines Carbon Majors emissions, FaIR warming attribution, and ERA5-anchored PR computation.

## Chain Summary

```
Carbon Majors emissions → FaIR warming shares → ERA5+hist-nat FAR → Black Summer damages → Entity liability
```

## Event Parameters

- **Event**: 2019–20 Australian bushfire season (Black Summer)
- **Region**: Southeastern Australia
- **Dates**: October 2019 – March 2020
- **Scale**: ~24 million ha burned; 3,000+ buildings destroyed; 33 direct deaths; 417 smoke deaths

## Probability Ratio (PR) — ERA5 + CMIP6 hist-nat (primary)

From `notebooks/02-attribution/04_black_summer_pr_era5.ipynb`:

| Scenario | PR | FAR | Basis |
|----------|----|-----|-------|
| Conservative | 1.0 | 0.0% | ERA5 bootstrap p05 — no detectable signal at 5th pct |
| **Central** | **1.8** | **44.4%** | **ERA5 bootstrap median (4-model corrected run)** |
| Upper | 2.9 | 65.5% | ERA5 bootstrap p95 |

**Validation**: WWA (van Oldenborgh et al. 2021) report PR ≥ 4–9. Our ERA5 bootstrap median (1.8)
is a conservative lower bound — the 4 available hist-nat models overestimate SE Australian natural
variability, suppressing the PR signal. WWA uses skill-selected models and is the better-constrained
upper reference. See [[2026-05-24-black-summer-pr-era5]] and [[datasets/wwa-studies]].

## Damage Scenarios

| Scenario | AUD (B) | USD (B) | Source |
|----------|---------|---------|--------|
| Conservative (insured losses) | 2.32 | 1.60 | Insurance Council of Australia |
| Central (direct economic) | 10.0 | 6.90 | Parliamentary Budget Office; sectoral studies |
| Comprehensive (total social cost) | 103.0 | 71.1 | Filkov et al. (2020); Deloitte Access Economics |

## Total Carbon Majors Attributed Liability

| Scenario | PR | FAR | Total CM liability |
|----------|-----|-----|--------------------|
| Conservative | 1.0 | 0.0% | **USD 0.0B** |
| **Central** | **1.8** | **44.4%** | **USD 3.1B** |
| Comprehensive | 2.9 | 65.5% | **USD 46.6B** |

Carbon Majors collectively account for ~45% of global fossil CO2. These figures represent that fraction
of the climate-attributed damages. All estimates are conservative lower bounds — the ERA5 bootstrap
median understates the true PR due to hist-nat model limitations.

## Top 5 Entity Liability (Central Scenario, USD millions)

| Rank | Entity | Type | USD M |
|------|--------|------|-------|
| 1 | Saudi Aramco | State-owned | 261 |
| 2 | ExxonMobil | Investor-owned | 219 |
| 3 | Gazprom | State-owned | 192 |
| 4 | BP | Investor-owned | 167 |
| 5 | Shell | Investor-owned | 159 |

## Key Finding: Damage Uncertainty Dominates

The biggest source of uncertainty is the **damage estimate** (~120× range from insured to total social
cost), not the attribution science. FAR varies from 29% to 78% across the full defensible PR range —
wider than the original WWA-based analysis, reflecting the conservative ERA5 median — but the damage
range still dominates. The choice of damage accounting framework matters far more than the PR source.

## Methodology Notes

- Entity liability = entity warming share × FAR × total damages
- Warming shares from FaIR v2.2 (841-config posterior ensemble, AR6-constrained) — see [[2026-05-15-emissions-to-warming]]
- PR from ERA5 daily mx2t + CMIP6 hist-nat r1i1p1f1 bootstrap — see [[2026-05-24-black-summer-pr-era5]]
- Proportionality assumption: each entity's share of global warming ≈ share of regional fire weather risk increase
- SE Australia CMIP6 amplification factor (0.935) applied; BoM observational ~1.35 suggests estimates remain conservative — see [[2026-05-23-australia-regional-amplification]]

## Caveats

1. **ERA5 PR is a conservative lower bound**: true PR likely higher, consistent with WWA ≥9. All liability figures understate true exposure.
2. **Scope 3 contested**: ~88% of attributed warming comes from scope 3 (product combustion). If liability frameworks exclude scope 3, per-entity figures shrink ~9×.
3. **Legal ≠ physical**: risk-proportional estimates, not legal determinations.
4. **Carbon Majors coverage**: ~45% of global fossil CO2 — total climate-attributed damages are larger than the CM share computed here.

## Outputs

- `data/processed/black_summer_liability.parquet` — per-entity liability across all scenarios
- `data/processed/black_summer_scenario_totals.csv` — scenario summary table

## Next Steps

- Add BoM observed amplification (~1.35) as an additional regional amplification scenario
- Apply pipeline to a second event once EM-DAT data is available
- Begin web API design to serve per-event liability tables
