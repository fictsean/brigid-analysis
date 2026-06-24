---
type: method
name: regional-amplification
tags: [amplification, regional, cmip6, era5, australia, fire-season, queensland, floods]
related: [far-probability-ratio, emissions-to-forcing, findings/2026-05-23-australia-regional-amplification, findings/2026-05-24-observed-amplification, findings/2026-05-26-qld-floods-regional-amplification, era5-reanalysis, cmip6, 2026-06-13-methodology-revision]
status: active
confidence: medium
last_updated: 2026-06-13
---

# Regional Amplification

The step between **global warming attribution** and **regional event risk** in the liability chain.
Entity warming shares are computed globally via FaIR (see [[methods/emissions-to-forcing]]). The
amplification factor α relates local to global warming, and **enters the pipeline as the shift
coefficient β in the GEV shift-fit** (see [[far-probability-ratio]]) — it does *not* multiply into
the final liability, which uses each entity's global warming share directly
([[2026-06-13-methodology-revision]]). The `warming_au_*` / `warming_qld_*` columns written by
notebooks 02/06 are diagnostic only.

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

Use CMIP6 historical runs to compare SE Australian warming to global GMST trend. This gives
a model-based estimate of how much the models predict the region will amplify global warming.

- Models: ACCESS-CM2, ACCESS-ESM1-5
- Metric: **annual-mean `tas`** (not fire-season tasmax), area-weighted over SE AU (28–44°S, 138–154°E)
- Period: 1901–2014
- Result: ensemble median **α = 0.935** (ACCESS-CM2 = 1.030, ACCESS-ESM1-5 = 0.841)

> The CMIP6 value is an **annual-mean** metric and is not directly comparable to the ERA5
> fire-season value below — this is why the ERA5 fire-season amplification is used as the primary β.

### ERA5 Observed (notebook 05)

Use ERA5 mx2t to compute the actual observed SE Australian fire-season warming and compare to
FaIR GMST trend over the same period.

- P1: ERA5 daily mx2t, fire-season (Oct–Mar) area-weighted mean, 1961–2020
- P0 (global): FaIR t_p50 (AR6-calibrated GMST), 1961–2020
- Both: linear regression trends, ratio = α
- Result: **α = 0.726** (SE AU trend +0.14°C/dec; global trend +0.20°C/dec)

## Current Values — SE Australia (Black Summer)

| Source | α | Metric | Period |
|--------|---|--------|--------|
| ACCESS-CM2 (CMIP6) | 1.030 | annual-mean tas / GMST | 1901–2014 |
| ACCESS-ESM1-5 (CMIP6) | 0.841 | annual-mean tas / GMST | 1901–2014 |
| CMIP6 ensemble median | 0.935 | annual-mean tas / GMST | 1901–2014 |
| **ERA5 observed (PRIMARY β)** | **0.726** | mx2t fire season / FaIR GMST | 1961–2020 |

## Current Values — SE Queensland (QLD Floods 2022)

Region: lat −30° to −24°S, lon 150° to 154°E. Season: wet season (Nov–Apr).

| Source | α | Metric | Period |
|--------|---|--------|--------|
| ACCESS-CM2 (CMIP6) | 0.364 | annual-mean tas / GMST | 1901–2014 |
| ACCESS-ESM1-5 (CMIP6) | 1.401 | annual-mean tas / GMST | 1901–2014 |
| CMIP6 ensemble median | 0.882 | annual-mean tas / GMST | 1901–2014 (only 2 models — p05/p95 are interpolation between two points, not a sampling range) |
| **ERA5 observed (PRIMARY β)** | **0.289** | mx2t wet season / FaIR GMST | 1961–2020 |

The ERA5 observed QLD value (0.289) is very low — wet-season land Tmax shows a weak trend in SE QLD
due to ENSO-driven variability and cloud cover feedback. Precipitation extremes respond more to
Coral/Tasman Sea SST than to land Tmax, so 0.289 understates the true warming forcing on QLD
flood extremes. See [[findings/2026-05-26-qld-floods-regional-amplification]].

## Which Value to Use

**SE Australia (Black Summer)**: The GEV shift-fit uses **β = α = 0.726** (ERA5 fire-season,
additive) as primary → PR = 4.0. CMIP6 α = 0.935 is a sensitivity (PR = 5.2).

**SE QLD (2022 Floods)**: The multiplicative shift-fit uses **β = ln(1+CC)·α** with **α = 0.289**
(ERA5 wet-season, conservative) as primary → PR = 1.11. CMIP6 α = 0.882 is a sensitivity (PR = 1.39).
See [[findings/2026-05-26-qld-floods-pr-era5]].

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

α enters the chain in **one** place — as the shift coefficient β in the PR computation
([[far-probability-ratio]]). A larger β produces a larger counterfactual shift and hence a higher
PR/FAR. This is a nonlinear dependence; α does **not** scale the liability linearly.

The final liability uses each entity's **global** warming share directly:

```
liability_USD = entity_global_warming_share × FAR(β) × total_damages
```

α would cancel if it were applied uniformly to both the entity and the regional total as a *share*,
which is why the per-region `warming_au_*` / `warming_qld_*` columns (notebooks 02/06) are retained
as diagnostics only and are **not** part of the liability calculation. (A previous version
incorrectly multiplied PR by an amplification *ratio* — see [[2026-06-13-methodology-revision]].)

## Caveats

- Two ACCESS models is a thin ensemble for SE Australia — a wider model ensemble would narrow
  the 0.841–1.030 spread
- The ERA5 vs CMIP6 discrepancy (0.726 vs 0.935) has not been resolved — it reflects genuine
  uncertainty in how to characterise regional amplification for this specific metric
- Future work: download BoM gridded temperature data and compute the same metric from station
  observations to provide a third independent estimate
