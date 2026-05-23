---
type: finding
name: 2026-05-23-australia-regional-amplification
tags: [cmip6, regional, australia, amplification, uncertainty, pangeo]
related: [2026-05-15-emissions-to-warming, 2026-05-18-black-summer-liability, cmip6, far-probability-ratio]
status: active
confidence: medium
last_updated: 2026-05-23
notebook: notebooks/02-attribution/02_australia_regional_amplification.ipynb
---

# Australian Regional Temperature Amplification — CMIP6 Ensemble

Computed the ratio of southeastern Australian warming to global mean warming from the CMIP6 historical ensemble, to validate and contextualise the use of global entity warming shares in Australian liability calculations.

## Method

- **Models**: ACCESS-CM2 and ACCESS-ESM1-5 (both Australian models, purpose-built for Australian climate)
- **Variable**: surface air temperature (`tas`), monthly, historical experiment
- **Region**: lat −44° to −28°S, lon 138° to 154°E (NSW/VIC/SA — matches WWA Black Summer study region)
- **Trend period**: 1901–2014 linear OLS trend
- **Baseline**: 1850–1900 anomaly

Data streamed from pangeo CMIP6 zarr stores — no local download required.

## Results

| Model | Global trend (°C/century) | SE AU trend (°C/century) | Amplification |
|-------|--------------------------|--------------------------|---------------|
| ACCESS-CM2 | 0.617 | 0.636 | 1.030 |
| ACCESS-ESM1-5 | 0.662 | 0.557 | 0.841 |
| **Ensemble median** | | | **0.935** |

## Key Finding: Models Underestimate Australian Warming

The CMIP6 ensemble gives an amplification factor of ~0.93 — SE Australia warming at slightly *below* the global mean rate in these models. This conflicts with observed data:

- **Bureau of Meteorology (observed)**: Australia has warmed ~1.47°C since 1910 vs ~1.09°C globally → amplification ≈ 1.35
- **CMIP6 ensemble (this analysis)**: amplification ≈ 0.93

This discrepancy is not unexpected. The WWA Black Summer study (van Oldenborgh et al. 2021) explicitly noted that "models underestimate the observed trend in heat" over Australia, and treated their PR values as conservative lower bounds for exactly this reason.

## Implications for Liability Estimates

Entity liability shares are **unchanged** — since all entities are scaled by the same amplification factor, their proportional contributions are identical whether expressed in global or regional warming terms.

What changes is the interpretation of magnitude: if the true Australian amplification is ~1.35 (observed) rather than ~0.93 (model), then actual entity warming contributions to SE Australia are ~45% larger than the CMIP6-derived figures suggest:

| Entity | Global warming (m°C) | CMIP6 AU (m°C, ×0.93) | Observed AU est. (m°C, ×1.35) |
|--------|---------------------|----------------------|-------------------------------|
| Saudi Aramco | 44.7 | 41.8 | 60.4 |
| ExxonMobil | 37.6 | 35.2 | 50.8 |
| Gazprom | 32.9 | 30.8 | 44.4 |

## Conservative Lower Bound

Using CMIP6-derived amplification (~0.93) means our liability estimates are **conservative lower bounds**, supported by the same model class the WWA study used. This is methodologically defensible: the underestimation bias is documented, peer-reviewed, and acknowledged by the attribution scientists themselves.

For litigation purposes, this means:
- Our central estimates can be presented as lower bounds
- The BoM-observed amplification (~1.35) supports a higher plausible estimate
- The gap between the two quantifies the model-underestimation uncertainty

## Outputs

- `data/processed/au_amplification_factor.csv` — per-model trend and amplification values
- `data/processed/entity_warming_contribution.parquet` — updated with `warming_au_p*/mdegC` columns
- `data/processed/black_summer_liability.parquet` — updated with `au_warming_share` and `liability_au_*` columns
- `outputs/figures/au_regional_amplification.png`

## Next Steps

- Add BoM observed amplification as an additional scenario in the Black Summer liability notebook
- When ERA5 zarr access is implemented, replace CMIP6-derived amplification with observed trend ratio for any region
- Apply same regional amplification pattern to future non-Australian events (each will have its own factor)
