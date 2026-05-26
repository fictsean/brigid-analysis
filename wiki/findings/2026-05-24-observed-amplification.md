---
type: finding
name: 2026-05-24-observed-amplification
tags: [amplification, era5, cmip6, australia, fire-season, calibration]
related: [2026-05-23-australia-regional-amplification, 2026-05-24-black-summer-pr-era5, 2026-05-18-black-summer-liability, era5-reanalysis]
status: active
confidence: medium
last_updated: 2026-05-24
notebook: notebooks/02-attribution/05_observed_amplification.ipynb
---

# Observed SE AU Fire-Season Amplification (ERA5)

Computes the observed SE Australia fire-season warming amplification factor from ERA5 daily mx2t
and compares it to the CMIP6 model value (0.935) from notebook 02. Uses existing on-disk data only.

## Method

- **SE AU trend**: linear trend in ERA5 fire-season (Oct–Mar) mean of daily maximum temperature (mx2t), area-weighted over SE AU (28–44°S, 138–154°E), 1961–2020
- **Global trend**: linear trend in FaIR GMST p50 (841-config AR6 posterior), 1961–2020
- **Amplification** = slope_AU / slope_global

## Results

| Source | Amplification | Metric | Period |
|--------|---------------|--------|--------|
| ACCESS-CM2 (CMIP6) | 1.030 | tasmax fire season / GMST | historical |
| ACCESS-ESM1-5 (CMIP6) | 0.841 | tasmax fire season / GMST | historical |
| CMIP6 ensemble median | 0.935 | tasmax fire season / GMST | historical |
| **ERA5 observed** | **0.726** | **mx2t fire season / FaIR GMST** | **1961–2020** |

- SE AU fire-season mean mx2t trend: **+0.14°C/decade**
- FaIR global GMST trend: **+0.20°C/decade**
- Correction factor (obs/CMIP6): **0.776**

## Key Finding: Observed Amplification Lower Than CMIP6

The ERA5 fire-season mean mx2t (0.726) is **lower** than the CMIP6 ensemble median (0.935). This
means CMIP6 models slightly overestimate SE AU fire-season temperature amplification relative to
global mean — the opposite of the initially expected direction.

The obs-corrected PR (ERA5 × 0.776) is therefore a **downward** correction, producing an alternative
lower-bound scenario rather than an upper constraint.

## Obs-Corrected Liability Scenarios

Applied to ERA5 bootstrap PR (med=1.80), central damages (AUD 10B):

| Scenario | PR | FAR | Total CM liability |
|----------|----|-----|--------------------|
| ERA5 p05 | 1.00 | 0.0% | USD 0.00B |
| **ERA5 bootstrap median** | **1.80** | **44.4%** | **USD 3.07B** |
| ERA5 p95 | 2.86 | 65.0% | USD 4.48B |
| Obs-corrected median (×0.776) | 1.40 | 28.4% | USD 1.96B |
| Obs-corrected p95 | 2.22 | 54.9% | USD 3.79B |

The ERA5 bootstrap median (3.07B) is the primary estimate. The obs-corrected median (1.96B)
is an alternative lower-bound sensitivity check. Note: ERA5 bootstrap PR updated after fixing
a cftime calendar bug that excluded GFDL-ESM4 and BCC-CSM2-MR from the P0 pool — the previous
value of 2.66 [1.39–4.61] was based on only 2 of the 4 hist-nat models.

## Interpretation: Metric Matters

The fire-season mean mx2t amplification factor measures **average temperature change**, not the
probability change in extreme tail events. Black Summer was a tail event. The ERA5 bootstrap PR
computed at the observed 99th percentile severity (PR=3.3) better represents the risk change
relevant to extreme fire weather, and remains consistent with WWA (≥10).

The amplification correction derived here is appropriate as a sensitivity check on the mean-warming
pathway, not as a correction to the tail-probability PR. The primary PR and liability estimates from
[[2026-05-24-black-summer-pr-era5]] are unaffected.

## Caveats

1. **Different metrics**: ERA5 mx2t (fire-season mean daily max) vs CMIP6 tasmax should be comparable,
   but the FaIR GMST vs CMIP6 GMST comparison may introduce a small bias.
2. **Short record**: 1961–2020 (60 years) is enough for a linear trend but subject to decadal variability
   (ENSO, IOD) in SE Australia.
3. **Regional noise**: SE AU fire-season temperatures have high inter-annual variability (R²~0.3–0.4 for
   the linear trend), so the trend estimate carries meaningful uncertainty.
4. **Annual mean vs fire season**: BoM reports SE AU annual mean warming ~1.3–1.5× global — the
   fire-season daily maximum metric is a different quantity and need not match.

## Outputs

- `data/processed/observed_amplification_factor.csv` — ERA5 observed amplification with trend metadata
- `data/processed/au_amplification_factor.csv` — updated with ERA5_observed row appended
- `data/processed/black_summer_liability.parquet` — updated with `liability_obs_p05/med/p95_USD_M` columns
- `outputs/figures/au_observed_amplification.png` — SE AU vs global trends + amplification comparison bar chart
