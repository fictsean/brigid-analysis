---
type: dataset
name: wwa-studies
tags: [attribution, far, pr, extreme-events, validation]
related: [emdat, methods/far-probability-ratio, cmip6]
status: stub
confidence: high
last_updated: 2026-05-14
---

# World Weather Attribution Studies

Published rapid attribution analyses by the World Weather Attribution (WWA) group (worldweatherattribution.org). Not a machine-readable database — a collection of event-specific PDF reports with supporting data. Use as validation targets and methodological reference.

## Key Facts

- Coverage: individual extreme events from ~2015 to present
- ~50+ published studies on heat waves, floods, droughts, hurricanes, wildfires
- Each study reports FAR and/or PR with confidence intervals
- Methodology is peer-reviewed and publicly documented

## Access

- All reports: worldweatherattribution.org/attribution-studies/
- Local path: `data/raw/wwa/` (PDFs + any supplementary CSVs)
- Key extracted values should be recorded in `wiki/disasters/` pages

## How to Use

WWA studies provide pre-computed attribution results for specific events. For events with WWA coverage:
1. Record the FAR/PR values in the event's `wiki/disasters/` page
2. Use as validation for our own pipeline on the same event
3. Use methodology notes as guidance for our approach

For events without WWA coverage, our pipeline needs to compute attribution from scratch using CMIP6 + ERA5.

## Key Methodological Papers

- Philip et al. (2020) "A protocol for probabilistic extreme event attribution analyses" — the WWA standard methodology
- Van Oldenborgh et al. — multiple foundational papers on PR-based attribution

## Caveats

- Studies vary in methodology over time as the field evolved — note study date
- Not all studies include economic damage attribution, only hazard attribution
- Some studies use regional climate models rather than global CMIP6

## Related

- [[methods/far-probability-ratio]] — methodology these studies implement
- [[disasters/]] — event pages that record extracted WWA values
