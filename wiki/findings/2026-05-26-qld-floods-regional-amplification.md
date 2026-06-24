---
type: finding
name: 2026-05-26-qld-floods-regional-amplification
description: SE QLD CMIP6 warming amplification α_QLD = 0.882 [0.416–1.349]; ERA5 observed = 0.289 (wet-season Tmax, conservative)
tags: [amplification, regional, queensland, cmip6, floods]
related: [findings/2026-05-23-australia-regional-amplification, findings/2026-05-24-observed-amplification, disasters/qld-floods-2022]
status: active
confidence: medium
last_updated: 2026-05-28
notebook: notebooks/02-attribution/06_qld_floods_regional_amplification.ipynb
---

# SE Queensland Regional Temperature Amplification

## Results

| Source | α_QLD | Notes |
|--------|-------|-------|
| ACCESS-CM2 (CMIP6 historical) | 0.364 | Low — QLD warms much less than global in this model |
| ACCESS-ESM1-5 (CMIP6 historical) | 1.401 | High — QLD warms faster than global |
| CMIP6 ensemble median | **0.882** | p05=0.416, p95=1.349 (only 2 models; MPI-ESM1-2-HR unavailable on pangeo) |
| ERA5 observed (wet-season Tmax) | **0.289** | 1961–2020; used as primary in notebook 07 |

Compare SE AU (notebook 02/05): CMIP6=0.935, ERA5=0.726.

## Method

Same approach as [[findings/2026-05-23-australia-regional-amplification]] (SE Australia):
- Region: lat −30° to −24°S, lon 150° to 154°E
- Variable: CMIP6 historical annual mean `tas`, `Amon`
- Trend period: 1901–2014; baseline: 1850–1900
- Amplification = QLD trend / global GMST trend

ERA5 observed (computed in notebook 07 Section 6):
- Variable: ERA5 daily maximum 2m temperature (mx2t), 06:00 UTC
- Season: wet-season (Nov–Apr) mean temperature
- Trend period: 1961–2020
- Amplification = QLD Tmax trend / FaIR GMST trend

## Key Caveats

1. **Only 2 CMIP6 models**: MPI-ESM1-2-HR was not available on pangeo for this run. Huge spread (0.364–1.401) reflects genuine model disagreement + small ensemble.

2. **ERA5 α_QLD = 0.289 is very low**: Wet-season maximum 2m temperature trend in SE QLD is 0.056°C/decade vs FaIR GMST 0.195°C/decade. This likely reflects ENSO-driven variability dampening the trend, and/or cloud cover feedback during the wet season. Compare with SE Australia fire-season (Oct–Mar): ERA5 = 0.726.

3. **Precipitation attribution uses land Tmax as scaling**: Technically, precipitation extremes respond more to atmospheric moisture content (driven by SST and lower-troposphere temperatures) than to land surface Tmax. Using land Tmax as the C-C scaling variable is conservative — the true warming relevant to QLD flood extremes is likely higher, giving a higher CC_factor and PR.

4. **Notebook 07 uses ERA5 observed** (0.289) as the primary amplification since it's observationally based. This is consistent with the approach in notebook 05 for Black Summer, where ERA5 observed (0.726) was preferred over CMIP6 (0.935).

## Implications for Liability

Using ERA5 α_QLD = 0.289:
- FaIR GMST shift 2022 vs 1961–1990: 1.034°C [p05=0.772, p95=1.351]
- Δ_QLD_T = 1.034 × 0.289 = 0.299°C
- CC_factor (7%/°C) = 1.021 → PR = 1.12, FAR = 10.5%

If CMIP6 median α_QLD = 0.882 were used:
- Δ_QLD_T = 1.034 × 0.882 = 0.912°C
- CC_factor (7%/°C) = 1.064 → meaningfully higher PR (not computed)

Entity warming shares (proportional) are unchanged from global. Total Carbon Majors QLD warming = 464.3 m°C (p50), vs global 526.1 m°C — ratio = α_QLD = 0.882.

## Outputs

- `data/processed/qld_amplification_factor.csv` — 3 rows (ACCESS-CM2, ACCESS-ESM1-5, ERA5_observed)
- `data/processed/entity_warming_contribution.parquet` — `warming_qld_p05/p50/p95_degC` columns appended
- `outputs/figures/qld_amplification.png`
