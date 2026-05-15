---
type: method
name: emissions-to-forcing
tags: [attribution, emissions, warming, liability]
related: [carbon-majors-database, far-probability-ratio, ekwurzel-2017]
status: stub
confidence: medium
last_updated: 2026-05-14
---

# Emissions to Forcing Attribution

How to translate an entity's historical emissions record into their proportional contribution to observed warming and sea level rise. This is the upstream step before event-level attribution.

## The Ekwurzel et al. (2017) Approach

The key precedent. Heede's Carbon Majors emissions data was fed into a simple climate model (MAGICC) to estimate each producer's contribution to:
- Observed global mean surface temperature rise (°C)
- Observed sea level rise (mm)
- Atmospheric CO2 concentration increase (ppm)

The proportional contribution of entity X is:
```
Contribution_X = Cumulative_emissions_X / Total_global_cumulative_emissions
```
Then applied to observed warming signal:
```
Warming_X = Contribution_X × Total_observed_warming
```

## Linear Proportionality Assumption

This approach assumes warming scales linearly with cumulative emissions — a reasonable approximation (supported by TCRE: Transient Climate Response to Cumulative CO2 Emissions) but with important caveats:
- CH4 has shorter atmospheric lifetime than CO2 — linear assumption less valid over long periods
- Ignores timing effects (early vs. late emissions have different atmospheric residence)
- Natural carbon sinks are treated as proportionally reducing all emitters equally

## Refinements to Consider

1. **Simple climate model (MAGICC/FAIR)**: run each entity's emission trajectory through a reduced-complexity climate model to get entity-specific forcing estimate
2. **Impulse response functions**: convolve emission pulse with atmospheric response function for better temporal accuracy
3. **Multi-gas weighting**: convert CH4, N2O to CO2e using GWP100 or GWP20 before summing

## Liability Fraction

```
Liability_fraction_X = Warming_X / Total_warming × FAR
```

This gives entity X's proportional contribution to the climate-change-attributed fraction of a specific disaster's damages.

## Key References

- Ekwurzel et al. (2017) — foundational calculation
- Matthews et al. (2009) — TCRE concept
- Meinshausen et al. (2011) — MAGICC model

## Related

- [[carbon-majors-database]] — source emissions data
- [[far-probability-ratio]] — downstream step: warming → event risk change
