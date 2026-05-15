---
type: method
name: far-probability-ratio
tags: [attribution, statistics, extreme-events]
related: [cmip6, era5-reanalysis, wwa-studies]
status: stub
confidence: high
last_updated: 2026-05-14
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

1. **Define the event**: characterize in terms of a threshold exceedance (e.g., 3-day precipitation total > X mm)
2. **Factual distribution (P1)**: fit a distribution to observations (ERA5) or model runs with all forcings (CMIP6 `historical`)
3. **Counterfactual distribution (P0)**: fit distribution to CMIP6 `hist-nat` (natural forcing only) runs
4. **Compute PR/FAR** with bootstrap or Bayesian uncertainty quantification

## Liability Application

FAR translates directly to the fraction of event damages attributable to anthropogenic climate change:

```
Climate-attributed damages = Total damages × FAR
```

The entity-level liability fraction then requires apportioning that climate-attributed fraction across emitters using their contribution to total forcing — see [[methods/emissions-to-forcing]].

## Caveats

- Results depend heavily on event definition and threshold choice
- Multi-model spread is a key source of uncertainty — use ensemble spread as structural uncertainty
- FAR > 0 does not imply the event was caused by climate change, only that the probability was increased

## Key References

- Philip et al. (2020) — WWA standard protocol
- Stott et al. (2016) — "Attribution of extreme weather and climate-related events"

## Related

- [[methods/emissions-to-forcing]] — upstream step: entity emissions → forcing contribution
- [[wwa-studies]] — pre-computed FAR/PR for specific events
- [[cmip6]] — counterfactual model runs
