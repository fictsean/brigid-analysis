---
type: method
name: far-probability-ratio
tags: [attribution, statistics, extreme-events, cmip6, gaussian, bootstrap]
related: [cmip6, era5-reanalysis, wwa-studies, 2026-05-18-black-summer-liability]
status: active
confidence: high
last_updated: 2026-05-26
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
2. **Factual distribution (P1)**: fit a distribution to ERA5 observed daily maximum temperature — the actual observed record, not a model simulation
3. **Counterfactual distribution (P0)**: fit distribution to CMIP6 `hist-nat` (natural forcing only) runs, r1i1p1f1 only to avoid ensemble imbalance
4. **Compute PR/FAR** with bootstrap uncertainty quantification

## ERA5 + CMIP6 hist-nat Implementation (Primary — Black Summer)

Notebook: `notebooks/02-attribution/04_black_summer_pr_era5.ipynb`

**P1 variable**: ERA5 `maximum_2m_temperature` (mx2t) at 06:00 UTC daily — 24-hour max covering the Australian afternoon peak. Monthly mean of daily max → Oct–Mar seasonal max anomaly.  
**P0 variable**: CMIP6 `tasmax` from `hist-nat` (r1i1p1f1 only), same pipeline applied.  
**Both P1 and P0 use the same metric**: monthly mean of daily maximum temperature — matches CMIP6 `tasmax` definition exactly.  
**Region**: SE Australia, lat −44° to −28°S, lon 138° to 154°E  
**Climatology baseline**: 1961–1990  
**Distribution**: Gaussian fit; uncertainty via 2,000-iteration bootstrap  
**Thresholds**: 90th, 95th, 97th, 99th percentile of the ERA5 P1 distribution; primary threshold = 2019 observed event anomaly  

**Why ERA5 for P1 (not CMIP6 historical)**: ERA5 is the observed record. Using CMIP6 historical for P1 embeds any model bias into the factual distribution, suppressing or inflating the PR signal depending on how the model handles regional warming. The standard WWA approach uses ERA5 for P1 for exactly this reason. See [[findings/2026-05-24-black-summer-pr-cmip6]] and [[methods/regional-amplification]] for the amplification context.

## Detrended ERA5 Implementation (Alternative P0)

Notebook: `notebooks/02-attribution/04_black_summer_pr_era5.ipynb` (Section 8)

Constructs P0 by shifting the ERA5 anomaly pool backwards by the estimated anthropogenic regional
warming signal Δ, rather than using CMIP6 hist-nat runs. This eliminates the model-variability
mismatch: CMIP6 hist-nat has slightly wider σ than ERA5, which suppresses PR. In this approach
P0 and P1 have identical σ, differing only by Δ.

```
Δ = (FaIR GMST₂₀₁₉ − mean FaIR GMST₁₉₆₁₋₁₉₉₀) × α_ERA5
  = 0.949°C × 0.726 = 0.689°C  [0.515–0.895 from FaIR p05–p95]
P0 pool = P1 pool − Δ
```

Bootstrap propagates ERA5 sampling uncertainty and FaIR shift uncertainty jointly.

**Result (Black Summer)**: PR = 3.8 [2.4–7.4], FAR = 73.6%, CM liability USD 5.1B. This is a
better central estimate than the CMIP6 hist-nat approach — it corrects for the model variability
bias while remaining consistent with the lower end of WWA (≥4). See [[findings/2026-05-24-black-summer-pr-era5]].

## CMIP6 hist vs hist-nat Implementation (Null Result — for reference)

Notebook: `notebooks/02-attribution/03_black_summer_pr_cmip6.ipynb`

Attempted hist vs hist-nat PR using CMIP6 tasmax. Failed: PR=0.6 [0.5–0.7]. Root causes: non-representative model subset, IPSL-CM6A-LR ensemble imbalance, CMIP6 historical underestimates Australian warming. See [[findings/2026-05-24-black-summer-pr-cmip6]].

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

## PR Sources — Black Summer 2019–20

| Source | PR | FAR | Role |
|--------|-----|-----|------|
| ERA5 + hist-nat (bootstrap median) | 1.80 [1.00–2.86] | 44.4% | Conservative lower bound — model variability bias suppresses PR |
| ERA5 + hist-nat (99th pct threshold) | 3.3 | 69.5% | — |
| **ERA5 detrended (bootstrap median)** | **3.8 [2.4–7.4]** | **73.6%** | **Better central estimate — corrects model variability bias** |
| WWA (van Oldenborgh 2021) FWI | ≥4 | ≥75% | Validation reference — peer-reviewed |
| WWA (van Oldenborgh 2021) MSR | ≥9 | ≥89% | Validation reference — peer-reviewed |
| CMIP6 hist vs hist-nat | 0.6 [0.5–0.7] | −0.66 | **Null result** — do not use |

The **detrended ERA5 approach (PR=3.8)** is the better central estimate. It corrects the CMIP6
hist-nat model-variability bias while remaining fully traceable and reproducible. Its bootstrap
range [2.4–7.4] is consistent with the WWA FWI lower bound (PR ≥ 4).

The **CMIP6 hist-nat run (PR=1.8)** is a conservative floor — defensible but understated because the
4 available models overestimate SE Australian natural variability.

WWA values serve as **validation reference** and upper bound. WWA uses models selected for Australian
skill; our approach uses whatever hist-nat runs are on pangeo.

For events without a WWA study, ERA5+hist-nat is the only available approach. For events with one, WWA confirms our estimates are in the right range.

## Caveats

- Results depend on event definition and threshold choice
- Multi-model spread is structural uncertainty; bootstrap captures sampling uncertainty within that spread
- Regional amplification is metric-dependent: CMIP6 models give SE AU fire-season amplification of 0.935 (relative to global mean); ERA5 observed fire-season mean mx2t gives 0.726. Neither is simply "right" — see [[methods/regional-amplification]]
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
