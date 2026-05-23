---
type: method
name: far-probability-ratio
tags: [attribution, statistics, extreme-events, cmip6, gaussian, bootstrap]
related: [cmip6, era5-reanalysis, wwa-studies, 2026-05-18-black-summer-liability]
status: active
confidence: high
last_updated: 2026-05-23
---

# Fraction of Attributable Risk (FAR) and Probability Ratio (PR)

The two core metrics used in probabilistic extreme event attribution. Both compare the probability of an event in the factual (observed) climate against a counterfactual climate without anthropogenic forcing.

## Definitions

**Probability Ratio (PR):**
```
PR = P1 / P0
```
Where P1 is the probability of the event in the factual climate and P0 in the counterfactual. PR = 2 means the event is twice as likely due to climate change.

**Fraction of Attributable Risk (FAR):**
```
FAR = 1 - (P0 / P1) = 1 - (1 / PR)
```
FAR is the fraction of the event's risk attributable to climate change. FAR = 0.5 means 50% of the event's risk is attributable.

## How P0 and P1 Are Estimated

1. **Define the event**: characterize in terms of a threshold exceedance (e.g., Oct–Mar seasonal max tasmax > Xth percentile)
2. **Factual distribution (P1)**: fit a distribution to CMIP6 `historical` runs (all forcings)
3. **Counterfactual distribution (P0)**: fit distribution to CMIP6 `hist-nat` (natural forcing only) runs
4. **Compute PR/FAR** with bootstrap uncertainty quantification

## CMIP6 Implementation (Black Summer)

Notebook: `notebooks/02-attribution/03_black_summer_pr_cmip6.ipynb`

**Variable**: `tasmax` (monthly mean of daily maximum temperature), `Amon` frequency  
**Region**: SE Australia, lat −44° to −28°S, lon 138° to 154°E (matches WWA Black Summer study area)  
**Metric**: Oct–Mar seasonal maximum anomaly relative to each model's 1961–1990 climatology  
**Models**: BCC-CSM2-MR, GFDL-ESM4, IPSL-CM6A-LR (10 hist-nat members), MRI-ESM2-0  
**Distribution**: Gaussian fit to pooled model anomalies  
**Uncertainty**: 2000-iteration bootstrap with random resampling of model ensemble  
**Thresholds**: 90th, 95th, 97th, 99th percentile of the historical distribution  

Removing the per-model climatology before pooling eliminates inter-model mean bias while preserving variance — standard practice in multi-model event attribution.

## Liability Application

FAR translates directly to the fraction of event damages attributable to anthropogenic climate change:

```
Climate-attributed damages = Total damages × FAR
```

The entity-level liability fraction then apportions that climate-attributed share across emitters using their warming contribution — see [[methods/emissions-to-forcing]].

In practice:
```python
liability_USD_M = entity_warming_share × far(pr) × total_damages_USD_M
```

## WWA vs CMIP6-Derived PR

| Source | PR (Black Summer heat) | FAR | Notes |
|--------|----------------------|-----|-------|
| WWA (van Oldenborgh 2021) | ≥4 (FWI) / ≥9 (MSR) | ≥0.75 / ≥0.89 | peer-reviewed, uses obs + models selected for AU performance |
| CMIP6 this analysis | 0.6 [0.5–0.7] | −0.66 | **null result** — available model subset does not reproduce AU warming signal |

WWA values are the authoritative source for Black Summer PR. The CMIP6 verification failed because the 4 models with both `historical` and `hist-nat` tasmax on pangeo are a non-representative subset with poor Australian regional performance and unbalanced ensemble members. See [[findings/2026-05-24-black-summer-pr-cmip6]].

For events without a published WWA study, CMIP6 PR computation may still be viable if models with demonstrated regional skill and balanced ensemble sizes are available.

## Caveats

- Results depend on event definition and threshold choice
- Multi-model spread is structural uncertainty; bootstrap captures sampling uncertainty within that spread
- CMIP6 models underestimate Australian heat trends — PR values from models are conservative lower bounds
- FAR > 0 does not imply causation, only that probability was increased

## Key References

- Philip et al. (2020) — WWA standard protocol
- van Oldenborgh et al. (2021) — Black Summer attribution, *Nat. Hazards Earth Syst. Sci.*
- Stott et al. (2016) — "Attribution of extreme weather and climate-related events"

## Related

- [[methods/emissions-to-forcing]] — upstream step: entity emissions → forcing contribution
- [[wwa-studies]] — pre-computed FAR/PR for specific events
- [[cmip6]] — counterfactual model runs
- [[2026-05-18-black-summer-liability]] — first application of FAR in liability chain
- [[2026-05-23-australia-regional-amplification]] — regional amplification context for PR estimates
