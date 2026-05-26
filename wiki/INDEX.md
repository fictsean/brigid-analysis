---
type: index
last_updated: 2026-05-26
---

# Wiki Index

Flat manifest of all pages. One line per page. Update this whenever a page is added or significantly changed.

---

## Meta
- [[CONTEXT]] — project overview, attribution chain, data sources, current phase
- [[ekwurzel-2017]] — Ekwurzel et al. (2017), foundational paper tracing warming to named producers via MAGICC

## Datasets
- [[datasets/carbon-majors-database]] — emissions by company-year 1854–present, Heede (2014), ~100 producers
- [[datasets/era5-reanalysis]] — ECMWF observed climate reanalysis, 1940–present, hourly global
- [[datasets/emdat]] — EM-DAT international disaster database, 1900–present, damages in USD
- [[datasets/cmip6]] — CMIP6 climate model ensemble outputs, historical + SSP scenarios
- [[datasets/wwa-studies]] — World Weather Attribution pre-computed FAR/PR studies

## Methods
- [[methods/attribution-chain]] — end-to-end overview: emissions → warming → PR → damages → liability (start here)
- [[methods/emissions-to-forcing]] — entity emissions → warming contribution via proportionality / FaIR
- [[methods/far-probability-ratio]] — FAR and PR definitions, ERA5+hist-nat implementation, liability application
- [[methods/regional-amplification]] — global → regional warming scaling; CMIP6 (0.935) vs ERA5 observed (0.726)

## Entities
*(none yet)*

## Disasters
- [[disasters/black-summer-2019-20]] — 2019–20 Australian bushfires; PR≥4; AUD 2.3–103B damages

## Concepts
*(none yet)*

## Models
*(none yet)*

## Findings
- [[findings/2026-05-15-carbon-majors-ingest]] — 1,435 GtCO₂e total; 13 entities = 50% of emissions; 69% post-1988; 88% scope 3
- [[findings/2026-05-15-emissions-to-warming]] — Saudi Aramco 44.7 m°C, ExxonMobil 37.6 m°C; Carbon Majors = 45% of total 1.18°C warming
- [[findings/2026-05-18-black-summer-liability]] — end-to-end chain; central: USD 3.1B CM liability (ERA5 PR=1.8, conservative lower bound); damage uncertainty dominates
- [[findings/2026-05-23-australia-regional-amplification]] — CMIP6 SE AU amplification = 0.93; models overestimate fire-season trend vs ERA5 (0.726); liability estimates are conservative lower bounds
- [[findings/2026-05-24-black-summer-pr-cmip6]] — CMIP6 hist vs hist-nat PR verification: null result (PR=0.6); available models don't reproduce Australian warming signal; WWA PR values stand
- [[findings/2026-05-24-black-summer-pr-era5]] — ERA5 daily mx2t: CMIP6 hist-nat P0 PR=1.8 (lower bound); detrended ERA5 P0 PR=3.8 [2.4–7.4] (central estimate); FAR 73.6%; USD 5.1B CM liability
- [[findings/2026-05-24-observed-amplification]] — ERA5 fire-season amplification = 0.726 (< CMIP6 0.935); obs-corrected liability 1.96B vs ERA5 central 3.07B; ERA5 bootstrap remains primary
- [[findings/2026-05-25-emdat-ingest]] — EM-DAT ingest; 17,849 records; Black Summer fragmented into sub-events (Currowan USD 2B); hardcoded Deloitte scenarios remain primary
