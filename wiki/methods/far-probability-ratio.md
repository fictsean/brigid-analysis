---
type: method
name: far-probability-ratio
tags: [attribution, statistics, extreme-events, gev, shift-fit, bootstrap, precipitation, clausius-clapeyron]
related: [cmip6, era5-reanalysis, wwa-studies, findings/2026-05-18-black-summer-liability, findings/2026-05-26-qld-floods-pr-era5, findings/2026-05-26-qld-floods-liability, 2026-06-13-methodology-revision]
status: active
confidence: high
last_updated: 2026-07-02
---

# Fraction of Attributable Risk (FAR) and Probability Ratio (PR)

The two core metrics in probabilistic extreme event attribution. Both compare the probability of an
event in the factual (observed) climate against a counterfactual climate without anthropogenic forcing.

## Definitions

**Probability Ratio**: `PR = P1 / P0` — P1 in the factual climate, P0 in the counterfactual.
PR = 2 means the event is twice as likely due to climate change.

**Fraction of Attributable Risk**: `FAR = 1 − P0/P1 = 1 − 1/PR`. FAR = 0.5 means 50% of the event's
risk is attributable.

## Method — Nonstationary GEV Shift-Fit (primary, both events)

> Revised 2026-06-13 ([[2026-06-13-methodology-revision]]). This replaces the earlier
> Gaussian/log-normal "ERA5 + CMIP6 hist-nat" and "detrended ERA5" approaches, which (a) mixed
> climatological baselines — the counterfactual removed only post-1961 warming, not warming since
> pre-industrial — and (b) evaluated parametric tails near the record maximum. The shift-fit is the
> standard WWA approach.

Implemented in `src/attribution/shift_fit.py` (`shift_fit_gev`), called by notebooks 04 and 07.

1. **Build one observed pool** of seasonal block maxima from ERA5 (no CMIP6 needed).
2. **Covariate**: smoothed FaIR GMST anomaly vs 1850–1900. The pre-industrial counterfactual
   covariate is therefore exactly **0**, so the shift removes *all* anthropogenic warming.
3. **Rescale** every season to a common climate using a shift coefficient β (the regional warming
   response):
   - **Additive** (temperature): x → x + β·(g_target − g_year), β in °C local per °C global.
   - **Multiplicative** (precipitation): x → x·exp(β·(g_target − g_year)), β = d(log x)/dg =
     ln(1+CC_rate)·α (C-C scaling × regional amplification).
4. **Fit a GEV** to the factual pool (shape ξ constrained to [−0.4, 0.4], WWA practice). Evaluate
   P1 at the observed event magnitude and P0 at the threshold mapped forward to the counterfactual
   climate.
5. **Bootstrap** (2,000×) resamples the season pool and jointly samples the FaIR event-year GMST
   uncertainty; β is refit each iteration when data-driven. `np.percentile` handles `inf` PR
   draws naturally (p95 is only inf if >5% of draws are essentially impossible counterfactuals).

**Why a GEV**: seasonal block maxima are extreme-value data; Gaussian/log-normal tails badly
mis-state exceedance probabilities exactly where the event sits. **Why ERA5 for the pool**: the
factual climate is the observed record, not a model's version of it.

## Results

### Black Summer 2019–20 (additive, mx2t)

| β (shift coefficient) | Source | PR | FAR | Role |
|-----------------------|--------|-----|-----|------|
| **0.726** | ERA5 fire-season amplification | **4.0 [2.4–15.4]** | **0.752** | **Primary** |
| 0.935 | CMIP6 annual-tas amplification | 6.3 [3.3–35] | 0.842 | Sensitivity |
| fitted (1.40) | data-driven OLS | 18.7 [5.5–154] | 0.947 | Rejected (outlier-driven, unstable) |
| — | WWA ERA5 FWI7x-SM (van Oldenborgh 2021) | >4 | >0.75 | Peer-reviewed validation |
| — | WWA model-FWI (conservative) | ≥1.3 | ≥0.23 | Context (models underestimate) |
| — | WWA heat-MSR | >9 | >0.89 | Peer-reviewed validation |

The primary (PR=4.0) sits at the WWA **ERA5 FWI7x-SM** lower bound (">4") — the observational metric,
not the model-based FWI ("≥30%").

### 2022 SE QLD Floods (multiplicative, precip 7-day max)

| β = ln(1+CC)·α | Source | PR | FAR | Role |
|----------------|--------|-----|-----|------|
| **0.0195** (7% × 0.289) | ERA5 wet-season amplification | **1.11 [1.05–1.30]** | **0.101** | **Primary — lower bound** |
| 0.0597 (7% × 0.882) | CMIP6 amplification | 1.39 [1.17–2.26] | 0.278 | Sensitivity |
| 0.0378 (14% × 0.289) | dynamic C-C | 1.23 [1.12–1.67] | 0.189 | Upper C-C sensitivity |
| 0.283 | data-driven fit | 4.78 | 0.791 | Rejected (ENSO-contaminated) |

No WWA study exists for this event; PR=1.11 is the only quantitative estimate, and a conservative one.

## Liability Application

```python
liability_USD = entity_global_warming_share × far(pr) × total_damages
```

FAR is the fraction of event damages attributable to anthropogenic climate change. The entity's
**global** warming share (not its share of the Carbon Majors subtotal) apportions that across
emitters — see [[emissions-to-forcing]] and [[2026-06-13-methodology-revision]].

## CMIP6 hist-nat (null result — reference only)

`notebooks/02-attribution/03_black_summer_pr_cmip6.ipynb` attempted hist vs hist-nat directly and
gave PR=0.6 (non-representative model subset, ensemble imbalance, CMIP6 underestimates AU warming).
Retained as a documented null result, not used for liability. The QLD hist-nat comparison was
similarly dropped — it lacked the quantile/bias correction needed to compare ERA5 and CMIP6
precipitation thresholds. See [[findings/2026-05-24-black-summer-pr-cmip6]].

## Caveats

- A single parametric GEV per pool; distribution-form uncertainty is not bootstrapped.
- Results depend on event definition, region, and the prescribed β.
- FAR > 0 indicates an increase in probability, not deterministic causation.

## Key References

- [[philip-2020]] — WWA standard protocol (shift-fit with covariate)
- [[van-oldenborgh-2021]] — Black Summer attribution, *NHESS*
- [[stott-2016]] — attribution of extreme weather events

## Related

- [[emissions-to-forcing]] — upstream: entity emissions → global warming share
- [[regional-amplification]] — source of the shift coefficient β
- [[wwa-studies]] — pre-computed FAR/PR for specific events
