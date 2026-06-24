---
type: finding
tags: [data-integrity, bug, carbon-majors, apportionment, liability]
related: [2026-06-13-methodology-revision, 2026-05-15-carbon-majors-ingest, 2026-05-15-emissions-to-warming, 2026-05-18-black-summer-liability, 2026-05-26-qld-floods-liability]
status: settled
confidence: high
last_updated: 2026-06-17
---

# LEI dropna data-loss bug — collective Carbon Majors share 44.6% → 75.5%

## Summary

The entity-year aggregation in `01-exploration/02_carbon_majors_ingest.ipynb` silently
discarded **~562 GtCO₂e** of emissions — every emitter whose `lei` (Legal Entity
Identifier) field is null. This understated every downstream warming share and liability
figure. Fixed 2026-06-17.

## The bug

```python
entity_year = df.groupby(["year", "parent_entity", "parent_type", "lei"]).agg(...)
```

Pandas `groupby` defaults to `dropna=True`, which drops **all rows where any grouping key
is NaN**. 5,870 of 20,054 raw rows have a null `lei`. Those rows — 562.5 GtCO₂e — never
made it into `cm_entity_year.parquet`, the primary input to the whole attribution chain.

The dropped emitters are not random; they are dominated by state actors and historical
entities that predate the LEI system:

| Entity | Dropped GtCO₂e |
|--------|----------------|
| Former Soviet Union (1900–1991) | 135.1 |
| China (Coal, 1945–2004) | 104.9 |
| Chevron | 62.5 |
| National Iranian Oil Company | 45.8 |
| China (Cement) | 25.1 |
| Poland (Coal) | 22.7 |
| British Coal Corporation | 19.7 |
| Kuwait Petroleum / Iraq NOC / Sonatrach / … | ~80 combined |

`1,435.6 − 562.5 = 873.1 GtCO₂e` — exactly the (buggy) parquet total, confirming the
mechanism.

## How it surfaced

The 2020 cumulative total from the buggy parquet (766 Gt) was ~half the raw 2024 total
(1,435.6 Gt), making it *look* as if half of all historical emissions occurred in
2021–2024. Physically impossible — the real 2020/2024 ratio is ~90%. Tracing that
discrepancy exposed the dropna drop.

The ingest notebook's *printed* key findings (1,435.6 Gt, Former Soviet Union #1) were
always correct because they compute from the raw `df`. Only the **saved parquet** was
corrupted — and that parquet is what every downstream notebook consumes.

## The fix

`lei` is provably constant per `parent_entity` (0 entities have multiple LEIs; 0 have
mixed null/non-null rows), so the minimal correct fix is `dropna=False` on that one
groupby — it keeps the null-LEI entities without splitting any entity:

```python
entity_year = df.groupby(
    ["year", "parent_entity", "parent_type", "lei"], dropna=False
).agg(...)
```

A conservation assertion was added immediately after (raw total == aggregated total) so
any future silent row loss fails loudly. This guard is the real lesson — the bug existed
because nothing checked that the aggregation preserved the emissions total.

## Impact

| Quantity | Before (buggy) | After (fixed) |
|----------|----------------|---------------|
| Entities in chain | 132 | 178 |
| Collective CM share of global fossil CO₂ | 44.6% | **75.5%** |
| Collective attributed warming (2020) | 0.53 °C | **0.89 °C** [0.66–1.19] |
| Black Summer central liability | USD 2.31B | **USD 3.92B** |
| QLD floods central liability | USD 0.31B | **USD 0.53B** |

The corrected 75.5% collective coverage is much closer to the documented ~71% Heede
figure than the buggy 44.6% — a sign the fix is directionally right. The small remaining
excess over 71% is attributable to the known **CO₂e-numerator vs CO₂-FFI-denominator
mismatch** (the numerator includes methane as CO₂e; the global denominator is fossil CO₂
only) — already on the next-steps list, separate from this bug.

## Key nuance: incumbents unchanged, headline driven by restored entities

This is **not** an across-the-board uplift. Entities that already had a valid LEI (Saudi
Aramco, ExxonMobil, BP, Shell) were never dropped, so their per-entity liabilities are
**unchanged** (Aramco: Black Summer USD 196.5M, QLD USD 27M [13–61] — same as before). The
entire headline increase comes from **restoring** the previously-dropped emitters —
notably Former Soviet Union (now #1), China Coal (#2), Chevron, and NIOC.

## Relationship to the global-share "halving"

This is fully **independent** of the 2026-06-13 global-share apportionment decision
([[2026-06-13-methodology-revision]]). That decision sets the *denominator* to all global
fossil CO₂ (so Carbon Majors absorb only their share of damages, not 100%). This bug
corrupted the *numerator* (entity emissions). Fixing it does not undo the global-share
convention — the global denominator is untouched; we simply stopped throwing away real
emissions. The two effects act on different parts of the calculation.

## Pipeline-hygiene fixes surfaced by re-running 02 + 06

Re-running the regional-amplification notebooks (to refresh the diagnostic `warming_au_*`/
`warming_qld_*` columns for all 178 entities) exposed three pre-existing issues, now fixed:

1. **Missing producer for QLD ERA5 α=0.289.** `nb07` reads `qld_af.loc['ERA5_observed']` from
   `qld_amplification_factor.csv`, but **no current notebook computes that row** — it is an orphan
   value (trend 0.056°C/decade vs FaIR GMST 0.195°C/decade; not reproducible from the SE QLD ERA5
   `mx2t` file under any standard wet-season definition). `nb06` overwrites the CSV with CMIP6-only
   rows, so its rerun silently deleted the row and would have broken `nb07` with a bare `KeyError`.
   Fixes: `nb06`'s save cell now **preserves** any externally-produced row (e.g. `ERA5_observed`);
   `nb07` now **fails loudly** with an actionable message if the row is absent. Reinstating a
   reproducible producer for α=0.289 is a tracked follow-up.

2. **AU vs QLD CSV conventions differ (by design).** `au_amplification_factor.csv` is CMIP6-only
   (`nb04` takes the median of all rows → 0.935; the AU ERA5 β=0.726 lives in
   `observed_amplification_factor.csv`). `qld_amplification_factor.csv` bundles the ERA5_observed
   row (`nb07` indexes it directly). So `nb02` dropping the AU ERA5 row was *correct*; `nb06`
   dropping the QLD ERA5 row was *not*. Documented to avoid future confusion.

3. **Stray display column leaked into the data artifact.** `nb02` assigned a millidegree display
   helper (`warming_au_p50_mdegC`) to `ew` before `to_parquet`. Removed from the save path and
   stripped from `entity_warming_contribution.parquet`.

## Files changed

- `notebooks/01-exploration/02_carbon_majors_ingest.ipynb` — `dropna=False` + conservation
  assertion; removed the unverifiable 1,421 GtCO₂e "launch report" benchmark (the 2026
  release publishes no headline total)
- Regenerated: `cm_entity_year.parquet`, `cm_cumulative_summary.parquet`,
  `entity_warming_contribution.parquet`, `black_summer_liability.parquet`,
  `qld_floods_liability.parquet`, and associated scenario-total CSVs
- Re-executed: `02-attribution/01_emissions_to_warming.ipynb`,
  `03-liability/01_black_summer_liability.ipynb`,
  `03-liability/02_qld_floods_liability.ipynb`
