---
type: finding
name: 2026-05-24-black-summer-pr-era5
tags: [era5, probability-ratio, black-summer, attribution, liability, gev, shift-fit]
related: [era5-reanalysis, cmip6, far-probability-ratio, 2026-05-24-black-summer-pr-cmip6, 2026-05-18-black-summer-liability, 2026-06-13-methodology-revision]
status: active
confidence: medium
last_updated: 2026-06-13
notebook: notebooks/02-attribution/04_black_summer_pr_era5.ipynb
---

# Black Summer PR — nonstationary GEV shift-fit

> **Revised 2026-06-13.** This analysis was reimplemented as a WWA-style **nonstationary GEV
> shift-fit** (see [[2026-06-13-methodology-revision]]). The earlier "ERA5 + CMIP6 hist-nat" and
> "detrended ERA5" Gaussian approaches are superseded — they mixed climatological baselines
> (counterfactual removed only post-1961 warming, not warming since pre-industrial) and evaluated
> Gaussian tails near the record maximum. The new method rescales the observed ERA5 record to the
> pre-industrial climate using a smoothed FaIR GMST covariate and fits a GEV to the seasonal block
> maxima. Numbers below are the revised values.

## Method

- **Factual / counterfactual** built from the **same** observed ERA5 pool, rescaled by the GMST
  covariate (anomaly vs 1850–1900, so the counterfactual covariate is exactly 0). No CMIP6
  streaming is required for the PR — fully reproducible from local ERA5 + the FaIR GMST parquet.
- **Distribution**: GEV fitted to fire-season (Oct–Mar) block maxima of monthly-mean daily-max
  mx2t, area-weighted over SE Australia (28–44°S, 138–154°E), shape ξ constrained to [−0.4, 0.4].
- **Shift coefficient β** (°C local per °C global) = the regional warming response. **Primary
  β = 0.726** (ERA5-observed fire-season amplification, notebook 05). The shift is additive:
  P0 evaluates the factual GEV at the threshold mapped forward by β·G₂₀₁₉.
- **Bootstrap**: 2,000 resamples of the season pool; FaIR event-year GMST uncertainty sampled
  jointly. Incomplete edge seasons are dropped (59 complete seasons, 1961–2019).

## Key Numbers (primary, β = 0.726)

| Metric | Value |
|--------|-------|
| Probability Ratio (bootstrap median) | **4.0** [5–95th: 2.4–15.4] |
| FAR | **0.752** [0.59–0.93] |
| GEV shape ξ | −0.21 (bounded upper tail) |
| 2019 anomaly | +1.30°C vs 1961–1990 (exceeded by 9 of 59 seasons) |
| Total Carbon Majors liability — central (AUD 10B) | **USD 3.92B** [3.07–4.87] (2026-06-17 LEI fix; see [[2026-06-17-lei-dropna-fix]]) |

The 2019 season is not the hottest in the record (2018 at +3.38°C is the outlier), so the PR
reflects a moderate-severity threshold, not the extreme tail.

## Sensitivities

| Shift coefficient β | Source | PR | FAR |
|---------------------|--------|-----|-----|
| **0.726** | ERA5 fire-season amplification | **4.0** [2.4–15.4] | **0.752** |
| 0.935 (→ fit 0.84) | CMIP6 annual-mean tas amplification | 5.2 [2.9–24] | 0.806 |
| fitted (1.40) | data-driven OLS on covariate | 18.7 [5.5–154] | 0.947 |

The data-driven fitted β (1.40) is dominated by the 2018 outlier season and produces an unstable
upper tail (the bounded GEV pushes the counterfactual probability toward zero), so it is **not**
used as the primary. The prescribed β=0.726 is stable and independently corroborated by WWA.

## Validation against WWA

WWA (van Oldenborgh et al. 2021) reported FWI PR ≥ 4 (FAR ≥ 0.75) and heat-MSR PR ≥ 9. The primary
shift-fit (PR = 4.0, FAR = 0.752) sits **exactly at the WWA FWI lower bound** — a much better
agreement than the superseded Gaussian approaches (hist-nat PR=1.8; detrended PR=3.8), and now on a
principled extreme-value footing referenced to pre-industrial.

## Outputs

- `data/processed/black_summer_pr_era5.csv` — PR table: primary + 2 sensitivities + WWA reference
- `data/processed/black_summer_pr_shiftfit_bootstrap.parquet` — 2,000 bootstrap PR samples (primary)
- `outputs/figures/black_summer_pr_shiftfit.png` — factual/counterfactual GEV + bootstrap histogram
- `data/raw/era5/era5_mx2t_daily_se_australia_1961_2020.nc` — ERA5 daily mx2t (83 MB, gitignored)

(Liability itself is computed in `notebooks/03-liability/01_black_summer_liability.ipynb`.)

## Caveats

- A single parametric GEV per pool; structural distribution-form uncertainty is not bootstrapped.
- β is prescribed from an independent amplification estimate; the data-driven fit is unstable for
  this 59-season record.
- Proportional attribution (TCRE linearity) applies as in upstream notebooks.

## Data Attribution

ERA5 data: Hersbach et al. (2023), DOI: 10.24381/cds.f17050d7. Contains modified Copernicus Climate
Change Service information. [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
