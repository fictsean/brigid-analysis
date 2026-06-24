---
type: finding
name: 2026-05-26-qld-floods-pr-era5
description: Multiplicative GEV shift-fit precip PR=1.11 [1.05–1.30], FAR=10.1% for 2022 QLD floods; conservative due to low ERA5 wet-season Tmax amplification
tags: [pr, far, attribution, precipitation, era5, queensland, floods, clausius-clapeyron, gev, shift-fit]
related: [findings/2026-05-24-black-summer-pr-era5, findings/2026-05-26-qld-floods-regional-amplification, disasters/qld-floods-2022, 2026-06-13-methodology-revision]
status: active
confidence: medium
last_updated: 2026-06-13
notebook: notebooks/02-attribution/07_qld_floods_pr_era5.ipynb
---

# ERA5 Precipitation Attribution — 2022 SE QLD Floods (GEV shift-fit)

> **Revised 2026-06-13** ([[2026-06-13-methodology-revision]]). Reimplemented as a **multiplicative
> nonstationary GEV shift-fit**, replacing the log-normal "detrended ERA5" approach. The
> counterfactual rescales each season's precipitation to the pre-industrial climate by
> exp(β·ΔG), β = ln(1+CC_rate)·α_QLD, with a GEV fitted to the 7-day block maxima. The CMIP6
> hist-nat cross-check is dropped from the primary path (it required a units/bias-correction not
> performed; see caveats). Result is essentially unchanged: PR ≈ 1.11.

## Key Results

| Method | β (d log P/dG) | PR | FAR | Role |
|--------|----------------|-----|-----|------|
| **CC 7%/°C × α=0.289 (ERA5)** | 0.0195 | **1.11 [1.05–1.30]** | **0.101** | **Primary — conservative lower bound** |
| CC 7%/°C × α=0.882 (CMIP6) | 0.0597 | 1.39 [1.17–2.26] | 0.278 | α sensitivity |
| CC 14%/°C × α=0.289 (dynamic) | 0.0378 | 1.23 [1.12–1.67] | 0.189 | Dynamic C-C upper |
| β fitted (data-driven) | 0.283 | 4.78 [1.40–32] | 0.791 | **Not used — ENSO-contaminated** |

## Method

- **Metric**: wet-season (Nov–Apr) maximum 7-day rolling precip, area-weighted over SE QLD
  (24–30°S, 150–154°E), 60 seasons (1962–2022).
- **Distribution**: GEV fitted to block maxima (ξ ≈ 0.08).
- **Counterfactual**: multiplicative log-space shift exp(β·ΔG_2022) with the smoothed FaIR GMST
  covariate (anomaly vs 1850–1900, extrapolated to 2022 since FaIR ends 2021).
- **2022 event**: 179.1 mm, rank 3/60.

## Key Caveats

1. **PR ≈ 1.11 is a conservative lower bound.** The limiting factor is α_QLD = 0.289 (ERA5
   wet-season land Tmax). SE QLD precipitation extremes respond more to Coral/Tasman Sea SST and
   lower-troposphere moisture than to land Tmax; SST amplification (~1.0) would give PR ≈ 1.3–1.5.
   The CMIP6 α=0.882 sensitivity (PR=1.39) brackets this.

2. **The data-driven fitted β (0.283 ≈ 28%/°C) is rejected.** It is ~4× the thermodynamic C-C rate
   and reflects ENSO-driven internal variability in a 60-season record, not a forced response.

3. **CMIP6 hist-nat dropped from the primary path.** The earlier comparison applied an
   ERA5-unit threshold to a CMIP6 distribution without bias correction (quantile mapping), so its
   PR=0.44 "null result" conflated a units/bias mismatch with a genuine model signal. A correct
   cross-check would require quantile-matched thresholds; not performed here.

4. **4×/day sampling proxy.** ERA5 tp downloaded at 00/06/12/18 UTC; the daily total uses these
   ×6. The scale factor cancels in the multiplicative PR (both climates use the same metric).

5. **No WWA study exists** for this event — PR ≈ 1.11 is the only quantitative estimate.

## Comparison to Black Summer

| | Black Summer | 2022 QLD Floods |
|---|---|---|
| Variable | ERA5 mx2t (additive) | ERA5 precip (multiplicative) |
| Shift coefficient β | 0.726 °C/°C | 0.0195 d log P/dG |
| PR (primary) | 4.0 [2.4–15.4] | 1.11 [1.05–1.30] |
| FAR (primary) | 0.752 | 0.101 |

## Outputs

- `data/processed/qld_floods_pr_era5.csv` — PR table (4 methods)
- `data/processed/qld_floods_pr_shiftfit_bootstrap.parquet` — 2,000 bootstrap PR samples (primary)
- `outputs/figures/qld_floods_pr_shiftfit.png`
