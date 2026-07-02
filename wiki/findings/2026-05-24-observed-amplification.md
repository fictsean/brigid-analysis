---
type: finding
name: 2026-05-24-observed-amplification
tags: [amplification, era5, cmip6, australia, fire-season, calibration]
related: [2026-05-23-australia-regional-amplification, 2026-05-24-black-summer-pr-era5, 2026-05-18-black-summer-liability, era5-reanalysis, 2026-06-13-methodology-revision]
status: active
confidence: medium
last_updated: 2026-07-02
notebook: notebooks/02-attribution/05_observed_amplification.ipynb
---

# Observed SE AU Fire-Season Amplification (ERA5)

> **Revised 2026-06-13** ([[2026-06-13-methodology-revision]]). The invalid `PR_obs = PR × (α_obs/α_cmip6)`
> correction and the `liability_obs_*` columns have been **removed**. PR is a nonlinear function of
> the distributional shift and does not scale linearly with an amplification ratio. The amplification
> factor enters correctly as the **shift coefficient β** in the GEV shift-fit (notebook 04). This
> notebook now (a) computes the observed fire-season amplification and (b) shows the *valid* β-sensitivity
> of the PR.

Computes the observed SE Australia fire-season warming amplification from ERA5 daily mx2t — the
physically meaningful coefficient β used as the primary additive shift in the Black Summer GEV
shift-fit ([[2026-05-24-black-summer-pr-era5]]). Uses on-disk data only.

## Method

- **SE AU trend**: linear trend in ERA5 fire-season (Oct–Mar) mean of daily-max temperature (mx2t),
  area-weighted over SE AU (28–44°S, 138–154°E), 1961–2020
- **Global trend**: linear trend in FaIR GMST p50, 1961–2020
- **Amplification β** = slope_AU / slope_global

## Results

| Source | β | Metric | Period |
|--------|---|--------|--------|
| **ERA5 observed** | **0.726** | **fire-season mean mx2t / FaIR GMST** | **1961–2020** |
| CMIP6 ensemble median | 0.935 | **annual-mean** tas / GMST | historical |

- SE AU fire-season mean mx2t trend: **+0.14°C/decade**; FaIR GMST trend: **+0.20°C/decade**

**The CMIP6 value (0.935) is an annual-mean tas amplification** (notebook 02), a *different metric*
from the ERA5 fire-season value — they are not directly comparable, which is why the fire-season
ERA5 estimate (0.726) is used as primary β and the CMIP6 value is only a sensitivity.

## β-Sensitivity of the Black Summer PR (the valid use of α)

Higher β → larger counterfactual shift → higher PR. This is the correct nonlinear dependence:

| β | Source | PR | FAR |
|---|--------|-----|-----|
| **0.726** | ERA5 fire-season (PRIMARY) | **4.0** [2.4–15.4] | **0.752** |
| 0.935 | CMIP6 annual tas | 6.3 [3.3–35] | 0.842 |

## Caveats

1. **Different metrics**: ERA5 fire-season mx2t vs CMIP6 annual-mean tas; the comparison of the two
   numbers reflects a metric difference, not a model error.
2. **Short record**: 1961–2020, subject to decadal variability (ENSO, IOD); regional fire-season
   trend R² ~0.3–0.4.
3. BoM reports SE AU *annual-mean* warming ~1.3–1.5× global — again a different quantity.

## Outputs

- `data/processed/observed_amplification_factor.csv` — ERA5 observed amplification with trend metadata
- `outputs/figures/au_observed_amplification.png`
