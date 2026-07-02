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
- [[disasters/black-summer-2019-20]] — 2019–20 Australian bushfires; GEV shift-fit PR=4.0, FAR=0.752; central CM liability USD 2.78B; AUD 2.3–103B damages
- [[disasters/qld-floods-2022]] — Feb–Mar 2022 SE Queensland floods; 676mm/3 days; AUD 5.56B insured; no WWA study; multiplicative GEV shift-fit PR=1.11 [1.05–1.30], FAR=0.101, central CM liability USD 0.38B

## Concepts
*(none yet)*

## Models
*(none yet)*

## References (papers — one page each, with article hyperlink)
- [[references/heede-2014]] — Carbon Majors tracing; 63% of industrial CO₂+CH₄ to 90 producers (10.1007/s10584-013-0986-y)
- [[references/ekwurzel-2017]] — warming/sea-level traced to producers; ~42–50% of GMST rise (10.1007/s10584-017-1978-0)
- [[references/stuart-smith-2025]] — Nature: systematic heatwave attribution to carbon majors; ~54% benchmark (10.1038/s41586-025-09450-9)
- [[references/stuart-smith-2025-liability]] — Nature: scientific case for climate liability (10.1038/s41586-025-08751-3)
- [[references/van-oldenborgh-2021]] — WWA Black Summer bushfire attribution (NHESS) (10.5194/nhess-21-941-2021)
- [[references/philip-2020]] — WWA probabilistic attribution protocol (ASCMO) (10.5194/ascmo-6-177-2020)
- [[references/stott-2016]] — review of extreme-event attribution (WIREs) (10.1002/wcc.380)
- [[references/matthews-2009]] — TCRE: warming ∝ cumulative carbon (Nature) (10.1038/nature08047)
- [[references/leach-2021]] — FaIRv2.0.0 climate emulator (GMD) (10.5194/gmd-14-3007-2021)
- [[references/smith-2024-fair-calibrate]] — fair-calibrate v1.4.1 posterior ensemble (GMD) (10.5194/gmd-17-8569-2024)
- [[references/meinshausen-2011]] — MAGICC6 emulator (ACP) (10.5194/acp-11-1417-2011)
- [[references/hersbach-2020]] — ERA5 global reanalysis (QJRMS) (10.1002/qj.3803)
- [[references/filkov-2020]] — Black Summer impacts/damages (J Saf Sci Resil) (10.1016/j.jnlssr.2020.06.009)
- [[references/comm-earth-env-2025-feb2022-floods]] — Feb 2022 extreme floods (Comm Earth Env) (10.1038/s43247-025-02307-z)
- [[references/jcli-2025-wet-2022]] — multiscale evaluation of wet 2022 E. Australia (J Climate) (10.1175/JCLI-D-24-0224.1)
- [[references/ipcc-ar6-wg1]] — IPCC AR6 WG1 physical science basis; ~1.07°C warming anchor

## Findings
- [[findings/2026-05-15-carbon-majors-ingest]] — 1,435 GtCO₂e total; 13 entities = 50% of emissions; 69% post-1988; 88% scope 3
- [[findings/2026-05-15-emissions-to-warming]] — Former Soviet Union 65.9 m°C, China Coal 51.1, Saudi Aramco 31.7 m°C; Carbon Majors = ~54% of total 1.18°C warming (total-CO₂ denominator)
- [[findings/2026-05-18-black-summer-liability]] — end-to-end chain; central USD 2.78B (GEV shift-fit PR=4.0, FAR=0.752, global-share apportionment); damage uncertainty (~44×) dominates
- [[findings/2026-05-23-australia-regional-amplification]] — CMIP6 SE AU amplification = 0.93 (annual-mean tas); ERA5 fire-season = 0.726 (primary β)
- [[findings/2026-05-24-black-summer-pr-cmip6]] — CMIP6 hist vs hist-nat PR verification: null result (PR=0.6); available models don't reproduce Australian warming signal; WWA PR values stand
- [[findings/2026-05-24-black-summer-pr-era5]] — nonstationary GEV shift-fit; primary β=0.726 → PR=4.0 [2.4–15.4], FAR=0.752; matches WWA ERA5 FWI7x-SM lower bound (PR>4)
- [[findings/2026-05-24-observed-amplification]] — ERA5 fire-season amplification = 0.726 (primary β); CMIP6 annual-tas 0.935 (sensitivity); invalid PR×ratio correction removed
- [[findings/2026-05-25-emdat-ingest]] — EM-DAT ingest; 17,849 records; Black Summer fragmented into sub-events (Currowan USD 2B); hardcoded PBO/ICA scenarios remain primary
- [[findings/2026-05-26-qld-floods-regional-amplification]] — CMIP6 α_QLD=0.882 (annual tas, 2 models); ERA5 observed=0.289 (wet-season Tmax, primary β)
- [[findings/2026-05-26-qld-floods-pr-era5]] — multiplicative GEV shift-fit: PR=1.11 [1.05–1.30], FAR=0.101; conservative; CMIP6 hist-nat dropped (units confound); 2022 = 3rd of 60 seasons
- [[findings/2026-05-26-qld-floods-liability]] — central USD 0.38B (AUD 10B × FAR=0.101); Saudi Aramco USD 19M; damage uncertainty dominates
- [[findings/2026-06-13-methodology-revision]] — **canonical record of methodology fixes**: global-share apportionment, GEV shift-fit, real uncertainty, removed PR×ratio; Black Summer 5.08B→2.31B
- [[findings/2026-06-17-lei-dropna-fix]] — **LEI dropna data-loss bug**: entity-year groupby dropped 562 GtCO₂e of null-LEI emitters; collective share 44.6%→75.5%; incumbents (Aramco) unchanged (later revised by the denominator fix)
- [[findings/2026-06-24-literature-cross-check]] — **literature cross-check + denominator fix**: collective warming 75.5%→53.6% (total-CO₂ FFI+AFOLU denominator; matches Stuart-Smith 2025 ~54%); Black Summer 3.92B→2.78B, QLD 0.53B→0.38B; added validation harness
- [[references/stuart-smith-2025]] — Nature 2025 carbon-majors heatwave attribution; primary external benchmark (~54% collective; Aramco ~0.04°C)
