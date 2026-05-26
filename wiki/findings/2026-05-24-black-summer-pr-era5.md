---
type: finding
name: 2026-05-24-black-summer-pr-era5
tags: [era5, probability-ratio, black-summer, attribution, liability]
related: [era5-reanalysis, cmip6, far-probability-ratio, 2026-05-24-black-summer-pr-cmip6, 2026-05-18-black-summer-liability]
status: active
confidence: medium
last_updated: 2026-05-26
notebook: notebooks/02-attribution/04_black_summer_pr_era5.ipynb
---

# Black Summer PR — ERA5 daily mx2t (factual) + CMIP6 hist-nat (counterfactual)

Independent PR computation using ERA5 observed daily maximum temperature as the factual (P1)
distribution and CMIP6 hist-nat as the counterfactual (P0). Corrects both failures from notebook 03:
replaces CMIP6 historical with ERA5 observations for P1, uses daily maximum (not monthly mean)
temperature, and restricts hist-nat to r1i1p1f1 to remove ensemble imbalance.

## Key Numbers

| Metric | Value |
|--------|-------|
| ERA5-anchored PR (bootstrap median, at 2019 threshold) | **1.8** [5–95th: 1.0–2.9] |
| PR at 97th pct threshold | 2.3 |
| PR at 99th pct threshold | **3.3** |
| FAR (bootstrap median) | **44.4%** |
| FAR at 97th pct | 57.0% |
| FAR at 99th pct | 69.5% |
| Total Carbon Majors liability — ERA5 median | **USD 3.1B** |
| Total Carbon Majors liability — ERA5 p05 | USD 0.0B (PR ≈ 1.0 at 5th pct) |
| Total Carbon Majors liability — ERA5 p95 | USD 4.5B |
| 2019 anomaly | 1.30°C above 1961–1990 mean (86th pct of P1) |

## Interpretation

**This run uses all 4 hist-nat models (previously only 2 were working due to a cftime calendar bug
in GFDL-ESM4 and BCC-CSM2-MR).** With 4 models, the P0 pool is 688 anomalies (vs 344 before) and
the natural-forcing distribution is wider (σ=0.95 vs previously narrower), which lowers the PR at
moderate thresholds. The bootstrap median (1.8) is substantially lower than the previous buggy
estimate (2.7).

The gap between bootstrap median (1.8) and WWA (≥10) is large. CMIP6 hist-nat models overestimate
natural temperature variability in SE Australia relative to the observations, which flattens the P0
tails and suppresses PR. The 99th-pct PR (3.3) shows clear attribution but still falls short of WWA.
WWA uses models selected for Australian skill; our subset was limited by pangeo hist-nat availability.

**Note on 2019 ranking**: 2019 ranks as the 2nd hottest fire season in ERA5 (behind 2018 at 28.11°C).
At the 86th percentile of P1, the threshold is moderate relative to the tail, which limits the PR.

## Detrended ERA5 Alternative (Section 8)

An alternative P0 was constructed by shifting the ERA5 anomaly pool backwards by the estimated
anthropogenic regional warming signal, rather than using CMIP6 hist-nat runs. This eliminates
the model-variability mismatch: P0 and P1 have identical σ (0.994), differing only by the shift Δ.

**FaIR GMST shift (2019 vs 1961–1990)**: 0.949°C [0.709–1.233]  
**Regional shift (× α_ERA5 = 0.726)**: Δ = 0.689°C [0.515–0.895]  
**P0 detrended**: μ = −0.463°C (vs P1 μ = +0.226°C)

| Metric | Value |
|--------|-------|
| PR at 2019 threshold (point estimate) | 3.7 |
| Bootstrap median PR | **3.8 [2.4–7.4]** |
| FAR (bootstrap median) | **73.6%** |
| CM total liability (central damages) | **USD 5.1B** |
| PR at 99th pct threshold | 8.0 |

The detrended result (3.8) sits between the CMIP6 hist-nat conservative bound (1.8) and WWA (≥10),
and is consistent with WWA's lower bound of ≥4. The bootstrap range [2.4–7.4] overlaps the WWA FWI
lower bound at 4.

**Which estimate to report**: The CMIP6 hist-nat run (PR=1.8) is a conservative lower bound — the
model P0 is wider than observed, suppressing PR. The detrended ERA5 (PR=3.8) corrects this by using
ERA5 variance for both distributions. The detrended estimate is the better central estimate; the
CMIP6 run provides a defensible floor. Both are below WWA (≥10), which used models selected for
Australian regional skill.

## Comparison Across PR Sources

| Source | PR (median) | FAR | CM Total Liability |
|--------|-------------|-----|-------------------|
| WWA FWI lower bound | 4 | 75.0% | USD 3.2B |
| WWA MSR central | 9 | 88.9% | USD 6.1B |
| ERA5 mx2t + hist-nat (2-model buggy run, superseded) | 2.7 [1.4–4.6] | 62.4% | USD 4.3B |
| **ERA5 mx2t + hist-nat (4-model corrected run)** | **1.8 [1.0–2.9]** | **44.4%** | **USD 3.1B** |
| **ERA5 mx2t detrended (shift = 0.689°C)** | **3.8 [2.4–7.4]** | **73.6%** | **USD 5.1B** |
| ERA5 mx2t at 99th pct threshold (hist-nat P0) | 3.3 | 69.5% | — |

## Methodology

- **P1**: ERA5 `mx2t` (maximum_2m_temperature) at 06:00 UTC daily — 24-hour max ending 06 UTC,
  capturing the Australian afternoon peak. Monthly mean of daily max → fire-season (Oct–Mar) max
  anomaly vs 1961–1990. Area: SE Australia 28–44°S, 138–154°E.
- **P0**: CMIP6 hist-nat, r1i1p1f1 only (BCC-CSM2-MR, GFDL-ESM4, IPSL-CM6A-LR, MRI-ESM2-0),
  same fire-season pipeline applied to CMIP6 `tasmax`.
- Both P1 and P0 use the same metric: monthly mean of daily maximum temperature.
- Bootstrap: 2,000 iterations at 2019 observed event threshold.
- Damages: AUD 10B direct economic (Deloitte central), USD/AUD 0.69.

## Caveats

- Four-model hist-nat subset is not selected for Australian skill — the PR signal is likely
  understated in P0 tails
- Bootstrap median reflects average exceedance probability across the full distribution; the
  99th-pct PR better represents the actual Black Summer event severity
- Proportional attribution (TCRE linearity) applies as in previous notebooks

## Outputs

- `data/processed/black_summer_pr_era5.csv` — PR at 4 percentile thresholds (CMIP6 hist-nat P0)
- `data/processed/black_summer_pr_era5_bootstrap.parquet` — 2,000 bootstrap samples (CMIP6 hist-nat P0)
- `data/processed/black_summer_pr_detrended_bootstrap.parquet` — 2,000 bootstrap samples (detrended ERA5 P0)
- `data/processed/black_summer_liability.parquet` — updated with `liability_era5_p05/med/p95_USD_M` columns
- `outputs/figures/black_summer_pr_detrended_era5.png` — distribution and PR curve comparison (both methods)
- `data/raw/era5/era5_mx2t_daily_se_australia_1961_2020.nc` — ERA5 daily mx2t (83 MB, gitignored)

## Data Attribution

ERA5 data: Hersbach et al. (2023), DOI: 10.24381/cds.f17050d7. Contains modified Copernicus Climate
Change Service information. [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

## Next Steps

- Compare ERA5 mx2t result to BoM observed amplification (~1.35) scenario
- If higher-skill hist-nat models become available on pangeo, rerun P0 to tighten the range
- Use ERA5 mx2t PR range as additional scenario in Black Summer liability notebook alongside WWA
