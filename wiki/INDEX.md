---
type: index
last_updated: 2026-05-30 (Black Summer liability notebook pipeline fix)
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
- [[disasters/black-summer-2019-20]] — 2019–20 Australian bushfires; GEV shift-fit PR=4.0, FAR=0.752; central CM liability USD 3.92B; AUD 2.3–103B damages
- [[disasters/qld-floods-2022]] — Feb–Mar 2022 SE Queensland floods; 676mm/3 days; AUD 5.56B insured; no WWA study; multiplicative GEV shift-fit PR=1.11 [1.05–1.30], FAR=0.101, central CM liability USD 0.53B

## Concepts
*(none yet)*

## Models
*(none yet)*

## Findings
- [[findings/2026-05-15-carbon-majors-ingest]] — 1,435 GtCO₂e total; 13 entities = 50% of emissions; 69% post-1988; 88% scope 3
- [[findings/2026-05-15-emissions-to-warming]] — Former Soviet Union 92.8 m°C, China Coal 72.0, Saudi Aramco 44.7 m°C; Carbon Majors = ~76% of total 1.18°C warming
- [[findings/2026-05-18-black-summer-liability]] — end-to-end chain; central USD 3.92B (GEV shift-fit PR=4.0, FAR=0.752, global-share apportionment); damage uncertainty (~44×) dominates
- [[findings/2026-05-23-australia-regional-amplification]] — CMIP6 SE AU amplification = 0.93 (annual-mean tas); ERA5 fire-season = 0.726 (primary β)
- [[findings/2026-05-24-black-summer-pr-cmip6]] — CMIP6 hist vs hist-nat PR verification: null result (PR=0.6); available models don't reproduce Australian warming signal; WWA PR values stand
- [[findings/2026-05-24-black-summer-pr-era5]] — nonstationary GEV shift-fit; primary β=0.726 → PR=4.0 [2.4–15.4], FAR=0.752; matches WWA FWI lower bound (PR≥4)
- [[findings/2026-05-24-observed-amplification]] — ERA5 fire-season amplification = 0.726 (primary β); CMIP6 annual-tas 0.935 (sensitivity); invalid PR×ratio correction removed
- [[findings/2026-05-25-emdat-ingest]] — EM-DAT ingest; 17,849 records; Black Summer fragmented into sub-events (Currowan USD 2B); hardcoded PBO/ICA scenarios remain primary
- [[findings/2026-05-26-qld-floods-regional-amplification]] — CMIP6 α_QLD=0.882 (annual tas, 2 models); ERA5 observed=0.289 (wet-season Tmax, primary β)
- [[findings/2026-05-26-qld-floods-pr-era5]] — multiplicative GEV shift-fit: PR=1.11 [1.05–1.30], FAR=0.101; conservative; CMIP6 hist-nat dropped (units confound); 2022 = 3rd of 60 seasons
- [[findings/2026-05-26-qld-floods-liability]] — central USD 0.53B (AUD 10B × FAR=0.101); Saudi Aramco USD 27M; damage uncertainty dominates
- [[findings/2026-06-13-methodology-revision]] — **canonical record of methodology fixes**: global-share apportionment, GEV shift-fit, real uncertainty, removed PR×ratio; Black Summer 5.08B→2.31B
- [[findings/2026-06-17-lei-dropna-fix]] — **LEI dropna data-loss bug**: entity-year groupby dropped 562 GtCO₂e of null-LEI emitters; collective share 44.6%→75.5%; Black Summer 2.31B→3.92B, QLD 0.31B→0.53B; incumbents (Aramco) unchanged
