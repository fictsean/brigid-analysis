---
type: method
name: regional-amplification
tags: [amplification, regional, cmip6, era5, australia, fire-season]
related: [far-probability-ratio, emissions-to-forcing, 2026-05-23-australia-regional-amplification, 2026-05-24-observed-amplification, era5-reanalysis, cmip6]
status: active
confidence: medium
last_updated: 2026-05-24
---

# Regional Amplification

The step between **global warming attribution** and **regional event risk** in the liability chain.
Entity warming shares are computed globally via FaIR (see [[methods/emissions-to-forcing]]). To
apply those shares to a regional event, we need to know how local warming relates to global warming.

## The Problem

If an entity is responsible for X% of global warming, their contribution to SE Australian warming
is not also X%. Different regions warm at different rates — some faster than the global mean
(amplified), some slower (damped). Applying the global share directly to a regional event
overstates or understates the regional contribution depending on direction.

**Amplification factor**:
```
α = regional_warming_trend / global_warming_trend
```

Entity's regional warming share = entity's global warming share × α

## How α Is Estimated

Two independent approaches have been applied to SE Australia for the Black Summer event:

### CMIP6 Historical (notebook 02)

Use CMIP6 historical runs to compare SE Australian tasmax trend to global GMST trend. This gives
a model-based estimate of how much the models predict the region will amplify global warming.

- Models: ACCESS-CM2, ACCESS-ESM1-5
- Metric: fire-season (Oct–Mar) tasmax, area-weighted over SE AU (28–44°S, 138–154°E)
- Period: full historical run (~1850–2014)
- Result: ensemble median **α = 0.935** (ACCESS-CM2 = 1.030, ACCESS-ESM1-5 = 0.841)

### ERA5 Observed (notebook 05)

Use ERA5 mx2t to compute the actual observed SE Australian fire-season warming and compare to
FaIR GMST trend over the same period.

- P1: ERA5 daily mx2t, fire-season (Oct–Mar) area-weighted mean, 1961–2020
- P0 (global): FaIR t_p50 (AR6-calibrated GMST), 1961–2020
- Both: linear regression trends, ratio = α
- Result: **α = 0.726** (SE AU trend +0.14°C/dec; global trend +0.20°C/dec)

## Current Values

| Source | α | Metric | Period |
|--------|---|--------|--------|
| ACCESS-CM2 (CMIP6) | 1.030 | tasmax fire season / GMST | historical |
| ACCESS-ESM1-5 (CMIP6) | 0.841 | tasmax fire season / GMST | historical |
| **CMIP6 ensemble median** | **0.935** | tasmax fire season / GMST | historical |
| **ERA5 observed** | **0.726** | mx2t fire season / FaIR GMST | 1961–2020 |

## Which Value to Use

The **CMIP6 ensemble median (0.935) is used in the primary liability calculation**. It is the
value embedded in the `entity_warming_contribution.parquet` `warming_au_*` columns.

The ERA5 observed value (0.726) is applied as an **obs-constrained sensitivity scenario**
(`liability_obs_*` columns in `black_summer_liability.parquet`). Because it is lower than the CMIP6
value, it produces a downward correction (obs-corrected central liability = USD 1.96B vs 3.07B).

## Why the Two Values Differ

This is a real methodological uncertainty, not an error in either approach.

1. **Metric mismatch**: The CMIP6 value uses model tasmax; the ERA5 value uses observed mx2t over
   a different calendar period (1961–2020 vs full historical). Conceptually the same variable, but
   the comparison period matters — decadal variability (ENSO, IOD) affects the trend slope.

2. **Annual vs fire-season**: BoM reports SE Australian *annual mean* temperature has warmed
   ~1.3–1.5× faster than global since 1910. That is a different metric. The fire-season daily
   maximum specifically over 1961–2020 shows the opposite: 0.726×. Fire-season temperature
   trends are sensitive to shifts in the subtropical ridge and ENSO teleconnections that may
   not dominate the annual mean signal.

3. **Natural variability**: The 60-year ERA5 record is noisy for a regional fire-season metric
   (linear regression R²~0.3). The CMIP6 models smooth over inter-annual variability by using the
   multi-model ensemble mean over a longer period.

4. **FaIR vs CMIP6 GMST**: The denominator matters. FaIR is calibrated to AR6 (best estimate
   GMST), which may warm faster over 1961–2020 than the specific CMIP6 models used in the
   numerator.

## How It Propagates Into Liability

```
entity_warming_au = entity_warming_global × α

liability_USD_M = entity_warming_au / total_warming_au × FAR × total_damages_USD_M
```

Equivalently (since total_warming_au = total_warming_global × α and the α cancels in the ratio):

```
liability_USD_M = entity_warming_share × FAR × total_damages_USD_M
```

The amplification factor only matters when comparing the **absolute warming contribution** of
an entity to a regional total — it cancels when expressed as a *share* of the regional warming,
which is the form used in the liability formula. The α term directly enters the PR correction
pathway instead (see [[methods/far-probability-ratio]]).

## Caveats

- Two ACCESS models is a thin ensemble for SE Australia — a wider model ensemble would narrow
  the 0.841–1.030 spread
- The ERA5 vs CMIP6 discrepancy (0.726 vs 0.935) has not been resolved — it reflects genuine
  uncertainty in how to characterise regional amplification for this specific metric
- Future work: download BoM gridded temperature data and compute the same metric from station
  observations to provide a third independent estimate
