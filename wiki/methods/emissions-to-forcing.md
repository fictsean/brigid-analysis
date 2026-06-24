---
type: method
name: emissions-to-forcing
tags: [attribution, emissions, warming, liability, fair]
related: [carbon-majors-database, far-probability-ratio, ekwurzel-2017, 2026-05-15-emissions-to-warming]
status: active
confidence: high
last_updated: 2026-05-24
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

## Implementation: FaIR v2.2

We use FaIR v2.2 (Finite Amplitude Impulse Response model) with the fair-calibrate v1.4 posterior ensemble (841 configs, constrained against IPCC AR6). This replaces MAGICC from Ekwurzel et al. (2017) with a more recent, better-constrained model.

Key implementation choices:
- **Proportional attribution** rather than per-entity model runs: entity_warming = (entity_cumulative_CO2e / global_cumulative_fossil_CO2) × FaIR_ΔT. Valid under TCRE linearity.
- **Global denominator**: RCMIP CO2 FFI historical emissions (consistent with Global Carbon Project)
- **Uncertainty**: 841-member posterior ensemble gives 5–95th percentile warming ranges
- **Validation**: FaIR median gives 1.04°C for 2011–2020 vs IPCC AR6 best estimate of 1.07°C ✓

**Known unit caveat**: the entity numerator is cumulative CO₂**e** (including operational CH₄ at
GWP-100) while the global denominator is CO₂ FFI only, and the share is applied to *total*
anthropogenic ΔT (which also includes land-use, non-fossil CH₄, and aerosol offsets). This modestly
inflates gas-heavy entities and the headline "~75% of warming" coverage figure (close to the ~71%
Heede figure; the excess is partly this unit mismatch). Within-Carbon-Majors rankings are largely
unaffected. A CO₂e-consistent denominator is a tracked follow-up.

See [[findings/2026-05-15-emissions-to-warming]] for results.

## Liability Fraction

```
Liability_X = global_warming_share_X × FAR × total_damages
            = (cumulative_CO2e_X / global_cumulative_fossil_CO2) × FAR × total_damages
```

Entity X is charged its share of **total global** warming — not its share of the Carbon Majors
subtotal. The named Carbon Majors collectively cover ~75% of global fossil CO₂, so they absorb ~75%
of the climate-attributed damages; the rest is attributable to emitters outside the database.
Normalising within the Carbon Majors group (so shares sum to 1) would over-charge every entity ~2.2×
— see [[2026-06-13-methodology-revision]]. Under TCRE linearity the FaIR ΔT cancels in the share
ratio, so the warming share equals the cumulative-emissions share.

## Key References

- Ekwurzel et al. (2017) — foundational calculation
- Matthews et al. (2009) — TCRE concept
- Meinshausen et al. (2011) — MAGICC model

## Related

- [[carbon-majors-database]] — source emissions data
- [[far-probability-ratio]] — downstream step: warming → event risk change
