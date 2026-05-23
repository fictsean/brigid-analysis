---
type: finding
name: 2026-05-24-black-summer-pr-cmip6
tags: [cmip6, pr, hist-nat, black-summer, australia, null-result]
related: [2026-05-18-black-summer-liability, 2026-05-23-australia-regional-amplification, far-probability-ratio, cmip6, wwa-studies]
status: active
confidence: high
last_updated: 2026-05-24
notebook: notebooks/02-attribution/03_black_summer_pr_cmip6.ipynb
---

# CMIP6 Independent PR Verification — Black Summer Heat (Null Result)

Attempted to compute the Probability Ratio (PR) for Black Summer 2019–20 heat independently from CMIP6 `historical` vs `hist-nat` experiments, as a cross-check against the WWA-published value of PR ≥ 10.

## Method

- **Variable**: `tasmax` (monthly mean of daily max temperature), `Amon`
- **Region**: SE Australia, lat −44° to −28°S, lon 138° to 154°E
- **Metric**: Oct–Mar fire season maximum tasmax anomaly (vs each model's 1961–1990 climatology)
- **Models**: BCC-CSM2-MR, GFDL-ESM4, IPSL-CM6A-LR (×10 hist-nat members), MRI-ESM2-0
- **Distribution**: Gaussian fit to pooled anomalies per experiment
- **Uncertainty**: 2,000-iteration bootstrap

## Results

| Threshold | P1 (historical) | P0 (hist-nat) | PR | FAR |
|-----------|----------------|---------------|-----|-----|
| 90th pct (0.97°C) | 0.098 | 0.146 | 0.67 | — |
| 95th pct (1.35°C) | 0.044 | 0.070 | 0.63 | — |
| 97th pct (1.63°C) | 0.022 | 0.036 | 0.60 | — |
| 99th pct (2.07°C) | 0.006 | 0.011 | 0.56 | — |

**Bootstrap (97th pct): PR = 0.6 [5–95th: 0.5–0.7]**

PR < 1 across all thresholds — these models show the counterfactual world as having *more* frequent extreme heat than the factual world. FAR is negative (meaningless). This is the opposite of the physical expectation and the WWA result.

## Why This Happened

**1. Non-representative model subset.** The 4 models available with both `historical` and `hist-nat` tasmax on pangeo were selected by data availability, not performance. They are not the models WWA used, and they are not known to perform well for Australian regional climate.

**2. Ensemble member imbalance.** IPSL-CM6A-LR contributes 10 hist-nat members but fewer historical members. Pooling creates an artificially wide hist-nat distribution with inflated variance, pushing P0 above P1 at high thresholds.

**3. Consistent with documented model bias.** Notebook 02 found CMIP6 models give SE Australia amplification 0.93 vs observed ~1.35. Models that underestimate the warming signal will fail to show a detectable PR. This is a known limitation explicitly acknowledged in the WWA Black Summer study itself.

## Implications

- **CMIP6 independent PR verification is not viable** with the currently available hist-nat tasmax subset on pangeo.
- **WWA PR values remain authoritative**: PR ≥ 4 (conservative), ≥ 9 (central), ≥ 15 (upper). These combine observations (ERA5) with models specifically selected for Australian performance.
- **Liability estimates are unaffected**: the `liability_cmip6_*` columns added to `black_summer_liability.parquet` should not be used. The WWA-based liability estimates stand.
- **Conservative framing is strengthened**: the CMIP6 model underestimation is now documented at two independent levels — regional warming (notebook 02) and event PR (this notebook). Both reinforce that our WWA-based estimates are lower bounds.

## What Would Be Needed for CMIP6 PR Verification

- Models with demonstrated skill for Australian tasmax (e.g. ACCESS-CM2, ACCESS-ESM1-5 — but these lack hist-nat tasmax on pangeo)
- Balanced ensemble members between historical and hist-nat experiments
- ERA5 observations combined with models (as WWA does) to anchor the factual distribution

## Outputs

- `data/processed/black_summer_pr_cmip6.csv` — PR at 4 thresholds (PR < 1, do not use for liability)
- `data/processed/black_summer_pr_bootstrap.parquet` — 2,000 bootstrap samples
- `data/processed/black_summer_liability.parquet` — `liability_cmip6_*` columns present but flagged as invalid
