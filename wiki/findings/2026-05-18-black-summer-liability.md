---
type: finding
name: 2026-05-18-black-summer-liability
tags: [black-summer, bushfire, australia, liability, far, fair, end-to-end]
related: [2026-05-15-carbon-majors-ingest, 2026-05-15-emissions-to-warming, far-probability-ratio, emissions-to-forcing, wwa-studies, 2026-05-24-black-summer-pr-era5, 2026-06-13-methodology-revision]
status: active
confidence: medium
last_updated: 2026-06-13
notebook: notebooks/03-liability/01_black_summer_liability.ipynb
---

# Black Summer 2019–20 — Entity Liability Estimates

> **Revised 2026-06-13** ([[2026-06-13-methodology-revision]]). Two corrections changed every
> number on this page: (1) apportionment now uses each entity's **global** warming share, not its
> share of the Carbon Majors subtotal — the previous code charged Carbon Majors 100% of attributed
> damages despite covering only their share of warming, inflating liability ~2.2×; (2) the PR is now
> the nonstationary GEV shift-fit (PR≈4.0), replacing the detrended Gaussian (PR=3.8). Net effect on
> the central estimate at the time: USD 5.08B → USD 2.31B.
>
> **Data fix 2026-06-17** ([[2026-06-17-lei-dropna-fix]]). The `cm_entity_year.parquet` aggregation
> was silently dropping ~562 GtCO₂e of null-LEI emitters (Former Soviet Union, China Coal, Chevron,
> NIOC…), understating collective coverage as 44.6%. Corrected to **75.5%**. Central liability
> USD 2.31B → **USD 3.92B**. Incumbents (Aramco, ExxonMobil) are unchanged; the rise comes entirely
> from the restored entities, which now lead the rankings.

End-to-end attribution chain applied to the 2019–20 Australian bushfire season. Combines Carbon
Majors emissions, FaIR warming attribution, and the GEV shift-fit PR.

## Chain Summary

```
Carbon Majors emissions → FaIR global warming shares → GEV shift-fit FAR → Black Summer damages → Entity liability
entity_liability = global_warming_share × FAR × total_damages
```

## Probability Ratio (PR)

Primary PR from the nonstationary GEV shift-fit (notebook 04, [[2026-05-24-black-summer-pr-era5]]):
**PR = 4.0 [2.4–15.4], FAR = 0.752**. This matches the WWA FWI lower bound (PR ≥ 4). Liability
uncertainty is propagated from the PR bootstrap; the FaIR ensemble cancels in every warming *share*
and so contributes no liability spread (see the methodology revision note).

## Damage Scenarios

The same primary FAR (0.752) is applied to each damage level — damages are the discrete damage
axis, kept separate from the PR axis (a joint PR × damages grid is in the notebook).

| Scenario | AUD (B) | USD (B) | Source |
|----------|---------|---------|--------|
| Conservative (insured losses) | 2.32 | 1.60 | Insurance Council of Australia |
| Central (direct economic) | 10.0 | 6.90 | Parliamentary Budget Office; sectoral studies |
| Comprehensive (total social cost) | 103.0 | 71.1 | Filkov et al. (2020); Deloitte Access Economics |

## Total Carbon Majors Attributed Liability

| Scenario | Damages | FAR [5–95%] | Total CM liability |
|----------|---------|-------------|---------------------|
| Conservative | AUD 2.3B | 0.752 [0.59–0.93] | **USD 0.91B** [0.71–1.13] |
| **Central (PRIMARY)** | **AUD 10B** | **0.752 [0.59–0.93]** | **USD 3.92B** [3.07–4.87] |
| Comprehensive | AUD 103B | 0.752 [0.59–0.93] | **USD 40.4B** [31.6–50.2] |

Carbon Majors collectively account for ~75% of global fossil CO₂; these figures are that fraction
of the climate-attributed damages. The remaining ~25% is attributable to emitters outside the
database. The 5–95% range is from the PR bootstrap.

## Top 5 Entity Liability — Central Scenario (USD millions)

| Rank | Entity | Type | USD M [5–95%] |
|------|--------|------|---------------|
| 1 | Former Soviet Union (1900–1991) | Nation State | 408 [319–507] |
| 2 | China (Coal, 1945–2004) | Nation State | 317 [248–394] |
| 3 | Saudi Aramco | State-owned | 197 [154–244] |
| 4 | Chevron | Investor-owned | 182 [142–226] |
| 5 | ExxonMobil | Investor-owned | 165 [130–206] |

Rankings are stable across all scenarios. (Former Soviet Union, China Coal and Chevron were absent
before the 2026-06-17 LEI fix — see [[2026-06-17-lei-dropna-fix]].)

## Key Finding: Damage Uncertainty Dominates

The biggest source of uncertainty remains the **damage estimate** (~44× range from insured to
total social cost), far larger than the PR/FAR uncertainty (FAR 5–95% spans 0.59–0.93, ~1.6×).

## Methodology Notes

- `entity_liability = global_warming_share × FAR × total_damages` (global-share apportionment)
- Warming shares from FaIR v2.2 (841-config AR6 posterior) — see [[2026-05-15-emissions-to-warming]]
- PR: nonstationary GEV shift-fit, primary β = 0.726 (ERA5 fire-season amplification)
- Regional amplification enters the PR as the shift coefficient β, **not** as a multiplier on
  liability — see [[regional-amplification]] and [[2026-06-13-methodology-revision]]

## Caveats

1. **PR is a defensible central estimate**, matching WWA FWI (PR≥4); WWA MSR (PR=9) implies higher
   exposure (FAR≈0.89 → ~USD 4.6B central).
2. **Scope 3 contested**: most attributed warming comes from product combustion. If liability
   frameworks exclude scope 3, per-entity figures shrink substantially (scope-1 sensitivity in
   notebook 01-exploration/01).
3. **Legal ≠ physical**: risk-proportional estimates, not legal determinations.
4. **Carbon Majors coverage**: ~75% of global fossil CO₂ — total climate-attributed damages are
   larger than the CM share computed here.

## Outputs

- `data/processed/black_summer_liability.parquet` — per-entity liability with `liability_<scenario>_USD_M`
  and `_p05_/_p95_` PR-uncertainty columns; `global_share` is the apportionment basis
- `data/processed/black_summer_scenario_totals.csv` — scenario summary with FAR 5–95%
