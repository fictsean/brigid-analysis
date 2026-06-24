---
type: dataset
name: wwa-studies
tags: [attribution, far, pr, extreme-events, validation]
related: [era5-reanalysis, cmip6, methods/far-probability-ratio, disasters/black-summer-2019-20]
status: active
confidence: high
last_updated: 2026-05-24
---

# World Weather Attribution Studies

Published rapid attribution analyses by the World Weather Attribution (WWA) group
(worldweatherattribution.org). Not a machine-readable database — a collection of event-specific
PDF reports with supporting data.

## Role in This Project: Validation

WWA studies are used as **validation references**, not as primary inputs to the liability pipeline.

The primary PR source for all liability calculations is our own **nonstationary GEV shift-fit** of
the observed ERA5 record (notebook `02-attribution/04_black_summer_pr_era5.ipynb`,
`src/attribution/shift_fit.py`), which is fully traceable, reproducible, and scalable to events
without a published WWA study.

Where a WWA study exists for the same event:
1. Compare our computed PR against WWA's published value
2. Agreement confirms the pipeline is sound; divergence flags a methodological issue to investigate
3. WWA is never used as a direct input to the liability formula

For Black Summer 2019–20, our GEV shift-fit (primary β=0.726) gives PR=4.0 [2.4–15.4], FAR=0.752 —
sitting **exactly at the WWA FWI lower bound** (PR ≥ 4). See [[findings/2026-05-24-black-summer-pr-era5]].

## Key Facts

- Coverage: individual extreme events from ~2015 to present
- ~50+ published studies on heat waves, floods, droughts, hurricanes, wildfires
- Each study reports FAR and/or PR with confidence intervals
- Methodology is peer-reviewed and publicly documented (Philip et al. 2020)
- Studies use ERA5, regional climate models, and CMIP6 — often with models selected for regional skill

## Access

- All reports: worldweatherattribution.org/attribution-studies/
- Local path: `data/raw/wwa/` (PDFs + any supplementary CSVs, if downloaded)
- Extracted key values are recorded in `wiki/disasters/` pages for each event

## Extracted Values by Event

| Event | Metric | PR | FAR | Source |
|-------|--------|----|-----|--------|
| Black Summer 2019–20 | Fire Weather Index (FWI) | ≥4 | ≥75% | van Oldenborgh et al. (2021) |
| Black Summer 2019–20 | Monthly Severity Rating (MSR) | ≥9 | ≥89% | van Oldenborgh et al. (2021) |
| Black Summer 2019–20 | Heat component | ~10 | ~90% | van Oldenborgh et al. (2021) |

## Key Methodological Papers

- Philip et al. (2020) "A protocol for probabilistic extreme event attribution analyses" — WWA standard methodology
- van Oldenborgh et al. (2021) — Black Summer attribution, *Nat. Hazards Earth Syst. Sci.*,
  DOI: 10.5194/nhess-21-941-2021

## Caveats

- Studies vary in methodology over time — note study date when comparing
- Not all studies include economic damage attribution, only hazard attribution
- Coverage is uneven — most studies focus on high-income countries or high-profile events
- Some studies use regional climate models rather than global CMIP6

## Related

- [[methods/far-probability-ratio]] — our PR methodology; WWA used as validation reference
- [[disasters/black-summer-2019-20]] — event page with extracted WWA values
- [[era5-reanalysis]] — primary data source for our own PR computation
