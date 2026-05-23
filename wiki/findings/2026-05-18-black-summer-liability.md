---
type: finding
name: 2026-05-18-black-summer-liability
tags: [black-summer, bushfire, australia, liability, far, fair, end-to-end]
related: [2026-05-15-carbon-majors-ingest, 2026-05-15-emissions-to-warming, far-probability-ratio, emissions-to-forcing, wwa-studies]
status: active
confidence: medium
last_updated: 2026-05-24
notebook: notebooks/03-liability/01_black_summer_liability.ipynb
---

# Black Summer 2019–20 — Entity Liability Estimates

First end-to-end run of the full attribution chain applied to a specific disaster. Combines Carbon Majors emissions data, FaIR warming attribution, and the WWA event attribution study for the 2019–20 Australian bushfire season.

## Chain Summary

```
Carbon Majors emissions → FaIR warming shares → WWA FAR → Black Summer damages → Entity liability
```

## Event Parameters

- **Event**: 2019–20 Australian bushfire season (Black Summer)
- **Region**: Southeastern Australia
- **Dates**: October 2019 – March 2020
- **Scale**: ~24 million ha burned; 3,000+ buildings destroyed; 33 direct deaths; 417 smoke deaths
- **Attribution source**: van Oldenborgh et al. (2021), *Nat. Hazards Earth Syst. Sci.* https://doi.org/10.5194/nhess-21-941-2021

## Probability Ratio (PR) and FAR

| Metric | PR | FAR | Notes |
|--------|-----|-----|-------|
| Fire Weather Index (FWI) | ≥4 | ≥0.75 | WWA lower bound; models underestimate observed heat trend |
| Monthly Severity Rating (MSR) | ≥9 | ≥0.89 | WWA central |
| Upper bound (model-corrected) | ~15 | ~0.93 | Plausible given explicit model underestimation caveat |

The WWA authors explicitly note that climate models underestimate the observed heat trend over Australia, meaning all PR values are conservative lower bounds.

## Damage Scenarios

| Scenario | AUD (B) | USD (B) | Source |
|----------|---------|---------|--------|
| Conservative (insured losses) | 2.32 | 1.60 | Insurance Council of Australia |
| Central (direct economic) | 10.0 | 6.90 | Parliamentary Budget Office; sectoral studies |
| Comprehensive (total social cost) | 103.0 | 71.1 | Filkov et al. (2020); Deloitte Access Economics |

Note: severe underinsurance in rural Australia means insured losses are a poor proxy for total economic impact.

## Total Carbon Majors Attributed Liability

| Scenario | Total damages | FAR | CM total liability |
|----------|--------------|-----|-------------------|
| Conservative | USD 1.60B | 75.0% | **USD 1.20B** |
| Central | USD 6.90B | 88.9% | **USD 6.13B** |
| Comprehensive | USD 71.07B | 93.3% | **USD 66.33B** |

Carbon Majors collectively account for ~45% of global fossil CO2. The above figures represent that fraction of the climate-attributed damages.

## Top 10 Entity Liability (Central Scenario, USD millions)

| Rank | Entity | Type | USD M |
|------|--------|------|-------|
| 1 | Saudi Aramco | State-owned | 521 |
| 2 | ExxonMobil | Investor-owned | 439 |
| 3 | Gazprom | State-owned | 384 |
| 4 | BP | Investor-owned | 334 |
| 5 | Shell | Investor-owned | 318 |
| 6 | Coal India | State-owned | 232 |
| 7 | Pemex | State-owned | 199 |
| 8 | ConocoPhillips | Investor-owned | 188 |
| 9 | CHN Energy | State-owned | 149 |
| 10 | Core Natural Resources | Investor-owned | 147 |

## Key Finding: Damage Uncertainty Dominates

The biggest source of uncertainty is the **damage estimate** (50× range from insured to total social cost), not the attribution science. FAR varies only from 75% to 93% across the full defensible PR range — a narrow band that changes total liability by ~25%. The choice of damage accounting framework matters far more.

This is important for litigation framing: debates about the attribution science are less consequential than debates about what counts as a compensable loss.

## Methodology Notes

- Entity liability = entity warming share × FAR × total damages
- Warming shares from FaIR v2.2 (841-config posterior ensemble, AR6-constrained) — see [[2026-05-15-emissions-to-warming]]
- Proportionality assumption: each entity's share of global warming = share of regional fire weather risk increase. This is an approximation; regional amplification factors not yet applied.
- PR baseline is ~1900 climate vs current, not a pure anthropogenic counterfactual — results are conservative
- Uncertainty bars in figures reflect FaIR ensemble spread only; emissions uncertainty and damage uncertainty shown as discrete scenarios

## Caveats

1. **Global vs regional attribution**: entity warming shares are global mean. A CMIP6-derived SE Australia amplification factor of 0.935 has been applied (notebook 02). BoM observations suggest true amplification is ~1.35, so estimates remain conservative lower bounds — see [[2026-05-23-australia-regional-amplification]].
2. **Scope 3 contested**: ~88% of attributed warming comes from scope 3 (product combustion). If liability frameworks exclude scope 3, per-entity figures shrink ~9×.
3. **Legal ≠ physical**: these are risk-proportional estimates, not legal determinations. Proximate cause, foreseeability, and jurisdictional standards all affect legal liability.
4. **Carbon Majors coverage**: ~45% of global fossil CO2, not 100% — total climate-attributed damages are larger than the CM share computed here.

## Outputs

- `data/processed/black_summer_liability.parquet` — 178 rows; all three liability scenarios per entity + FaIR uncertainty bounds
- `data/processed/black_summer_scenario_totals.csv` — scenario summary table
- `outputs/figures/black_summer_liability_top20.png`
- `outputs/figures/black_summer_scenario_comparison.png`
- `outputs/figures/black_summer_sensitivity_aramco.png`

## Next Steps

- Apply the same pipeline to additional events (extend to a catalogue once EM-DAT is available)
- Replace WWA-borrowed PR with ERA5-anchored PR once CDS API key is set up — see [[2026-05-24-black-summer-pr-cmip6]]
- Model scope 1-only liability as an alternative for legally conservative estimates
- Begin web API design to serve per-event liability tables
