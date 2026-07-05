---
type: disaster
name: qld-floods-2022
tags: [flood, australia, queensland, precipitation, 2022]
related: [era5-reanalysis, cmip6, emdat, far-probability-ratio, findings/2026-05-26-qld-floods-regional-amplification, findings/2026-05-26-qld-floods-pr-era5, findings/2026-05-26-qld-floods-liability]
status: active
confidence: medium
last_updated: 2026-07-05
---

# 2022 SE Queensland Floods

## Event Summary

- **Dates**: February–March 2022 (peak: 26 February – 3 March 2022)
- **Region**: SE Queensland (Brisbane, Ipswich, Sunshine Coast, Gold Coast) and Northern NSW
- **Peak precipitation**: Brisbane recorded 676.8 mm in 3 days (February 26–28) — a record
- **Insurance claims**: ~236,000 (Insurance Council of Australia)
- **Direct deaths**: 13 (Queensland); ~22 total including NSW
- **Cause**: Slow-moving low-pressure system over SE QLD; enhanced by La Niña and record warm
  sea-surface temperatures in the Coral Sea and Tasman Sea

## Attribution

### No WWA Published Study
No World Weather Attribution (WWA) rapid attribution study — and no probabilistic (PR) attribution study of any kind — was published for this event (confirmed June 2026), so our PR=1.11 remains the sole quantitative estimate. Attribution is built from ERA5 precipitation using a multiplicative (Clausius-Clapeyron) GEV shift-fit (see [[methods/far-probability-ratio]] and notebook 07).

Two 2025 papers characterise the event qualitatively (both emphasising La Niña + warm SST drivers, consistent with our conservative framing) but give no PR: *How February 2022 redefines extreme floods in Australia* (Communications Earth & Environment, doi:10.1038/s43247-025-02307-z) and *A Multiscale Evaluation of the Wet 2022 in Eastern Australia* (Journal of Climate, JCLI-D-24-0224.1).

### Multiplicative GEV Shift-Fit (Primary)
**Source**: `notebooks/02-attribution/07_qld_floods_pr_era5.ipynb`; `src/attribution/shift_fit.py`

**Method**: GEV fitted to wet-season (Nov–Apr) 7-day-max precip block maxima, SE QLD box
(−30° to −24°S, 150° to 154°E), 1962–2022. The pool is rescaled to the pre-industrial climate by
exp(β·ΔG), β = ln(1+CC_rate)·α_QLD, with the smoothed FaIR GMST covariate. See
[[2026-06-13-methodology-revision]] for the change from the earlier log-normal approach.

| Method | PR | FAR | Notes |
|--------|-----|-----|-------|
| **CC 7%/°C × α=0.289 (ERA5)** | **1.11 [1.05–1.30]** | **0.101** | **Primary — conservative lower bound** |
| CC 7%/°C × α=0.882 (CMIP6) | 1.39 [1.17–2.26] | 0.278 | α sensitivity |
| CC 14%/°C × α=0.289 (dynamic) | 1.23 [1.12–1.67] | 0.189 | Dynamic C-C upper |

**Note**: PR is conservative — driven by ERA5 wet-season land Tmax amplification = 0.289 (very low). Precipitation extremes respond more to SST/atmospheric moisture; the CMIP6 α sensitivity (PR=1.39) brackets a more realistic value. The CMIP6 hist-nat cross-check was dropped — it lacked the quantile/bias correction needed to compare ERA5 and CMIP6 precip thresholds.

See [[findings/2026-05-26-qld-floods-pr-era5]] for full results.

### QLD Regional Amplification
SE QLD warming amplification factor α_QLD computed from CMIP6 historical annual mean `tas`
(ACCESS-CM2, ACCESS-ESM1-5, MPI-ESM1-2-HR) relative to global GMST, 1901–2014.

See [[findings/2026-05-26-qld-floods-regional-amplification]].

## Damages

**Verified 2026-07-05** (superseding the earlier AUD 10B / 20B placeholders, which had no source).

| Estimate | AUD (B) | Source | Scope | Status |
|----------|---------|--------|-------|--------|
| Insured losses (final) | 5.81 | Insurance Council of Australia, 240,000+ claims (published Apr 2023) | **QLD + NSW** | Confirmed |
| **Total cost (economic + social)** | **7.7** | **Deloitte Access Economics** for the QLD Government / QLD Reconstruction Authority, June 2022 (23 LGAs, Gladstone→Gold Coast→Balonne) | **QLD only** | Confirmed |
| — of which tangible/direct | ~3.2 | homes & commercial buildings AUD 2.0B (~18,000 properties); small business AUD 0.32B; agriculture AUD 0.25B; public infrastructure & other ~AUD 0.65B | QLD only | Confirmed |
| — of which intangible/social | 4.5 | human & social cost, >500,000 people affected | QLD only | Confirmed |

The **Deloitte AUD 7.7B** is the authoritative anchor for this event: it was commissioned by the
Queensland Government, covers exactly our SE QLD event footprint (QLD only), and is the only
published *total-cost* study of the event. The ICA AUD 5.81B is insured losses for the wider
QLD+NSW event, so it is a scope-mismatched lower bound (insured < total; QLD is the bulk of the
event, so it remains internally consistent as a floor).

> **The earlier AUD 10B "direct economic" central and AUD 20B "comprehensive" figures were
> unsourced placeholders — no source supports them.** As of 2026-07-05 the pipeline uses
> **conservative AUD 5.81B (ICA insured) + central AUD 7.7B (Deloitte total cost)**; the AUD 20B
> comprehensive scenario was retired. See [[findings/2026-07-05-qld-damage-verification]].

**EM-DAT note**: Records only USD ~726M (fragmented into sub-events — same fragmentation issue as
Black Summer). Independently-sourced ICA/Deloitte/government figures are primary; EM-DAT is an
internal cross-check only and must **not** be surfaced in a public app (see [[datasets/emdat]]).

## Liability Analysis

See [[findings/2026-05-26-qld-floods-liability]] for full entity-level breakdown.

Central scenario (AUD 7.7B Deloitte total cost, PR=1.11, FAR=0.101):
- **Total Carbon Majors attributed liability: USD 0.29B**
- Former Soviet Union USD 30M, China Coal USD 24M, Saudi Aramco USD 14.6M [7.5–33], ExxonMobil USD 12M
- Apportioned by each entity's **global** warming share (~54% CM coverage = entity CO₂ / total
  anthropogenic CO₂ FFI+AFOLU; see [[findings/2026-06-24-literature-cross-check]]); α_QLD enters via
  the PR shift coefficient β, not as a liability multiplier

## Methodological Notes

This event uses precipitation attribution (C-C multiplicative scaling) rather than temperature
attribution (additive shift used for Black Summer). Key differences:
- **Distribution**: log-normal for precipitation (vs Gaussian for tasmax)
- **Counterfactual**: P0 = P1 / CC_factor (multiplicative, log-space)
- **Metric**: 7-day rolling maximum total precipitation in wet season (Nov–Apr)
- **FaIR extrapolation**: FaIR GMST parquet ends at 2021; 2022 value extrapolated via linear
  trend on 2010–2021 data (documented as approximation)

## Litigation Context

The 2022 SE QLD floods occurred shortly after Australia passed the Climate Change Act 2022
(legislating 43% emissions reduction by 2030). The floods contributed to political pressure
around the government's climate response and were cited in subsequent state planning decisions around floodplain development in SE Queensland.
