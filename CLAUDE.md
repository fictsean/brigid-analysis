# brigid-analysis — Project Context for Claude

## What This Project Does

Builds climate attribution models that quantify the liability of specific polluting entities (Carbon Majors, state actors) with respect to specific climate disasters. The end goal is a web application that can accept a disaster as input and return a structured liability breakdown with uncertainty ranges.

## The Attribution Chain

Each analysis traverses this chain, propagating uncertainty at each step:

```
Named Emitter → Cumulative Emissions → Atmospheric Forcing → Climate Signal → Event P(risk) Change → Damages → Liability Fraction
```

1. **Emissions record**: Carbon Majors database (Heede 2014, updated by Climate Accountability Institute) — traces ~71% of global emissions to ~100 producers
2. **Forcing → warming**: IPCC AR6 best estimates; CMIP6 model ensemble outputs via pangeo/ESGF
3. **Event attribution**: Fraction of Attributable Risk (FAR) and Probability Ratio (PR) methods; draws on World Weather Attribution (WWA) published studies where available
4. **Damages → liability**: Novel part — proportional contribution to observed warming × fraction of damages attributable to climate change

## Repo Layout

```
data/raw/          # never edited; large files gitignored
data/processed/    # cleaned, joined outputs
data/sources.md    # provenance log for every dataset
notebooks/01-exploration/
notebooks/02-attribution/
notebooks/03-liability/
notebooks/99-scratch/
src/attribution/   # Python modules extracted from notebooks
src/data/
src/models/
outputs/figures/
outputs/reports/
wiki/              # Obsidian vault — LLMwiki
CLAUDE.md          # this file
```

## Wiki Structure

The `wiki/` directory is an Obsidian vault following the LLMwiki pattern — files are written to be consumed as LLM context, not just read by humans.

- `wiki/CONTEXT.md` — project overview (load first in any LLM session)
- `wiki/INDEX.md` — flat manifest of all pages
- `wiki/entities/` — Carbon Majors companies, state actors
- `wiki/disasters/` — specific climate events
- `wiki/datasets/` — one page per data source
- `wiki/methods/` — attribution methodologies
- `wiki/findings/` — dated research conclusions from notebooks
- `wiki/concepts/` — scientific, legal, economic terms
- `wiki/models/` — ML/statistical models built

Frontmatter schema used across wiki pages:
```yaml
type: entity | disaster | dataset | method | finding | concept | model
tags: [...]
related: [other-page-slugs]
status: stub | active | settled
confidence: low | medium | high
last_updated: YYYY-MM-DD
```

## Key External Resources

- Carbon Majors database: carbonmajors.org (InfluenceMap) — free download, T&C click-through required
- WWA studies: worldweatherattribution.org
- CMIP6 data: pangeo (preferred, cloud zarr) or ESGF nodes
- ERA5 reanalysis: Copernicus Climate Data Store (CDS) — free account + `~/.cdsapirc` key required
- Disaster records: EM-DAT (emdat.be) — downloaded; `data/raw/emdat/emdat_global_natural.csv` (22.9 MB, gitignored)
- Key paper: Ekwurzel et al. (2017) "The rise in global atmospheric CO2, surface temperature, and sea level from emissions traced to major carbon producers"
- FaIR model: https://github.com/OMS-NetZero/FAIR — v2.2 with fair-calibrate v1.4 posterior (841 configs)

## Conventions

- Notebooks are numbered and named: `01-exploration/02_carbon_majors_ingest.ipynb`
- Every notebook that produces a meaningful result gets a corresponding `wiki/findings/YYYY-MM-DD-slug.md` page
- All uncertainty estimates are expressed as 5th–95th percentile ranges unless stated otherwise
- Physical attribution (contribution to risk) is kept strictly separate from legal liability framing
- Processed data saved as parquet; figures saved to `outputs/figures/` (gitignored)

## Standing instructions
- At the end of any updates, review and update any relevant wiki pages, the claude.md file and the readme.md file.
- After running a notebook update the key findings section.

## Completed Work (as of 2026-06-09)

### Data
- `data/raw/carbon_majors/emissions_high_granularity.csv` — downloaded, 178 entities 1854–2024
- CMIP6 — streamed on demand from pangeo zarr (no local download needed)
- ERA5 daily mx2t (SE Australia) — downloaded, `data/raw/era5/era5_mx2t_daily_se_australia_1961_2020.nc` (83 MB, gitignored)
- ERA5 total precipitation (SE QLD) — downloaded, `data/raw/era5/era5_tp_daily_se_qld_1961_2022.nc` (20.9 MB, gitignored); 4x/day sampling (00/06/12/18 UTC), downloaded in 7 decade batches to stay within CDS quota limits
- ERA5 daily mx2t (SE QLD) — downloaded, `data/raw/era5/era5_mx2t_daily_se_qld_1961_2020.nc` (9.6 MB, gitignored)
- EM-DAT — downloaded; `data/raw/emdat/emdat_global_natural.csv` (22.9 MB, gitignored)

### Notebooks
1. `01-exploration/01_environment_check.ipynb` — verifies all packages and pangeo connectivity
2. `01-exploration/02_carbon_majors_ingest.ipynb` — loads Carbon Majors, produces entity-year and cumulative summary parquets
3. `01-exploration/03_emdat_ingest.ipynb` — loads EM-DAT CSV, normalises columns, CPI-adjusts damages to 2020 USD, saves parquet; 17,849 natural disaster records; Black Summer validation shows EM-DAT splits event into sub-events (Currowan: USD 2B), so hardcoded PBO/ICA scenarios remain primary for Black Summer
4. `02-attribution/01_emissions_to_warming.ipynb` — FaIR v2.2 warming attribution, 841-config AR6 posterior ensemble
5. `02-attribution/02_australia_regional_amplification.ipynb` — CMIP6 historical SE AU amplification factor; ACCESS-CM2 + ACCESS-ESM1-5
6. `02-attribution/03_black_summer_pr_cmip6.ipynb` — independent PR computation from CMIP6 hist vs hist-nat; null result PR=0.6; do not use for liability
7. `02-attribution/04_black_summer_pr_era5.ipynb` — **nonstationary GEV shift-fit** (thin caller of `src/attribution/shift_fit.py`); primary β=0.726 → PR=4.0 [2.4–15.4], FAR=0.752; sensitivities β=0.935 (PR=5.2) and fitted (PR=18.7, rejected); fully local (no CMIP6 streaming)
8. `02-attribution/05_observed_amplification.ipynb` — ERA5 observed SE AU fire-season amplification = 0.726 (primary β); CMIP6 annual-tas = 0.935 (sensitivity); shows valid β-sensitivity of PR (invalid PR×ratio correction removed)
9. `03-liability/01_black_summer_liability.ipynb` — end-to-end chain (thin caller of `build_liability_table`); **global-share apportionment**; primary PR=4.0, FAR=0.752 → central USD 3.92B; conservative/central/comprehensive damage scenarios share the primary FAR; PR-bootstrap uncertainty
10. `02-attribution/06_qld_floods_regional_amplification.ipynb` — SE QLD warming amplification (annual-mean tas); CMIP6 median α_QLD=0.882 (only 2 models — p05/p95 are interpolation, not sampling); ERA5 observed wet-season Tmax α_QLD=0.289 (primary β); `warming_qld_*` columns are diagnostic only (not used in liability)
11. `02-attribution/07_qld_floods_pr_era5.ipynb` — **multiplicative GEV shift-fit** for 2022 SE QLD floods; 2022=3rd of 60 wet seasons; primary CC 7%/°C × α=0.289 → PR=1.11 [1.05–1.30], FAR=0.101 (conservative lower bound); sensitivities CMIP6 α=0.882 (PR=1.39), dynamic 14%/°C (PR=1.23); fitted β rejected (ENSO-contaminated); CMIP6 hist-nat dropped (units confound)
12. `03-liability/02_qld_floods_liability.ipynb` — QLD floods end-to-end liability; global-share apportionment; central USD 0.53B (AUD 10B × FAR=0.101); Saudi Aramco central USD 27M [13–61] (incumbent entities ~unchanged by the LEI fix); EM-DAT REDACTED-DISNO (value redacted, EM-DAT DUA) supports AUD 10B as plausible

### Source modules
- `src/attribution/shift_fit.py` — `shift_fit_gev`, `fit_gev`: nonstationary GEV shift-fit (additive + multiplicative)
- `src/attribution/liability.py` — `build_liability_table`, `far`: global-share apportionment + PR-bootstrap uncertainty
- `src/attribution/seasonal.py` — `area_weighted_series`, `season_block_max`, `wet_season_max_ndays`
- `src/attribution/gmst.py` — FaIR GMST covariate helpers (load, extrapolate, smooth, event sigma)
- `src/attribution/constants.py` — `AUD_TO_USD` (keyed by year), CC rates, climatology baseline
- `src/data/emdat.py` — `load_emdat()`, `search_events()`, `get_event_damages()` helpers
- `scripts/build_notebooks.py` — regenerates notebooks 04/05/07/01-liab/02-liab as thin callers and executes them

### Key processed files
- `data/processed/cm_entity_year.parquet` — entity × year emissions
- `data/processed/cm_cumulative_summary.parquet` — cumulative totals and global share per entity
- `data/processed/entity_warming_contribution.parquet` — per-entity warming (p05/p50/p95), `global_share` (apportionment basis), + warming_au_*/warming_qld_* (diagnostic only)
- `data/processed/fair_global_temperature.parquet` — FaIR ensemble temperature timeseries
- `data/processed/au_amplification_factor.csv` — per-model SE AU amplification (annual-mean tas): ACCESS-CM2 1.030, ACCESS-ESM1-5 0.841, median 0.935, ERA5_observed 0.726 (fire-season)
- `data/processed/qld_amplification_factor.csv` — per-model SE QLD amplification (annual-mean tas): ACCESS-CM2 0.364, ACCESS-ESM1-5 1.401, median 0.882, ERA5_observed 0.289 (wet-season)
- `data/processed/black_summer_liability.parquet` — entity liability; `global_share` + `liability_<scenario>_USD_M` + `_p05_/_p95_` PR-uncertainty columns
- `data/processed/black_summer_pr_era5.csv` — GEV shift-fit PR table (primary + 2 sensitivities + WWA reference)
- `data/processed/black_summer_pr_shiftfit_bootstrap.parquet` — 2,000 bootstrap PR samples (primary, β=0.726)
- `data/processed/black_summer_pr_cmip6.csv` + `black_summer_pr_bootstrap.parquet` — CMIP6 null-result reference (PR=0.6 — do not use)
- `data/processed/observed_amplification_factor.csv` — ERA5 observed SE AU amplification with trend metadata
- `data/processed/qld_floods_pr_era5.csv` — QLD floods GEV shift-fit PR table (4 methods)
- `data/processed/qld_floods_pr_shiftfit_bootstrap.parquet` — 2,000 bootstrap PR samples (primary)
- `data/processed/qld_floods_liability.parquet` — entity rows, QLD floods liability by scenario
- `data/processed/qld_floods_scenario_totals.csv` — scenario-level totals for QLD floods
- `data/processed/emdat_disasters.parquet` — cleaned EM-DAT natural disasters, 17,849 records (gitignored — EM-DAT Data Use Agreement)

### Wiki pages
- `wiki/disasters/qld-floods-2022.md` — 2022 SE QLD floods event summary, attribution, damages, liability, litigation context
- `wiki/findings/2026-05-15-carbon-majors-ingest.md`
- `wiki/findings/2026-05-15-emissions-to-warming.md`
- `wiki/findings/2026-05-18-black-summer-liability.md`
- `wiki/findings/2026-05-23-australia-regional-amplification.md` — CMIP6 SE AU amplification 0.935 (ACCESS-CM2, ACCESS-ESM1-5)
- `wiki/findings/2026-05-24-black-summer-pr-cmip6.md` — CMIP6 PR verification null result (PR=0.6); available hist-nat model subset does not reproduce AU warming signal; WWA PR values stand
- `wiki/findings/2026-05-24-black-summer-pr-era5.md` — GEV shift-fit; primary β=0.726 → PR=4.0 [2.4–15.4], FAR=0.752; matches WWA FWI lower bound
- `wiki/findings/2026-05-24-observed-amplification.md` — ERA5 fire-season amplification = 0.726 (primary β); CMIP6 annual-tas 0.935 (sensitivity); invalid PR×ratio correction removed
- `wiki/findings/2026-05-25-emdat-ingest.md` — EM-DAT ingest; 17,849 records; Black Summer fragmented into sub-events (Currowan USD 2B); hardcoded PBO/ICA scenarios remain primary
- `wiki/findings/2026-05-26-qld-floods-regional-amplification.md` — CMIP6 α_QLD=0.882 (annual tas, 2 models); ERA5 observed=0.289 (wet-season Tmax, primary β)
- `wiki/findings/2026-05-26-qld-floods-pr-era5.md` — multiplicative GEV shift-fit: PR=1.11 [1.05–1.30], FAR=0.101; CMIP6 hist-nat dropped (units confound); 2022=3rd of 60 seasons
- `wiki/findings/2026-05-26-qld-floods-liability.md` — central USD 0.53B (AUD 10B × FAR=0.101); Saudi Aramco USD 27M; damage uncertainty dominates
- `wiki/findings/2026-06-13-methodology-revision.md` — **canonical record of the methodology fixes**: global-share apportionment, GEV shift-fit, real uncertainty, removed PR×ratio; Black Summer 5.08B→2.31B
- `wiki/findings/2026-06-17-lei-dropna-fix.md` — **LEI dropna data-loss bug**: entity-year groupby silently dropped 562 GtCO₂e of null-LEI emitters (Former Soviet Union, China Coal, Chevron, NIOC…); collective share 44.6%→75.5%; Black Summer 2.31B→3.92B, QLD 0.31B→0.53B; incumbent entities (Aramco) ~unchanged

## Current Status / Next Steps

End-to-end pipeline proven on two events and refactored into `src/attribution/` (notebooks are thin
callers). See `wiki/findings/2026-06-13-methodology-revision.md` for the full list of corrections.

**Black Summer**: nonstationary GEV shift-fit, primary β=0.726 → PR=4.0 [2.4–15.4], FAR=0.752,
central Carbon Majors liability **USD 3.92B** (global-share apportionment). Matches WWA FWI lower bound (PR≥4).

**QLD Floods 2022**: multiplicative GEV shift-fit, primary PR=1.11 [1.05–1.30], FAR=0.101, central
Carbon Majors liability **USD 0.53B** (AUD 10B damages placeholder). Conservative lower bound — driven
by low ERA5 wet-season land Tmax amplification (α_QLD=0.289); CMIP6 α=0.882 sensitivity gives PR=1.39.
Central damages (AUD 10B) still need verification from QLD Treasury / Deloitte / NEMA.

**Apportionment convention**: liability = entity **global** warming share × FAR × damages. Carbon
Majors collectively cover **~75%** of the global fossil-CO₂ denominator (close to the ~71% Heede
figure; the ~75% is slightly inflated by the known CO₂e-numerator vs CO₂-FFI-denominator mismatch —
see next steps), so they absorb ~75% of climate-attributed damages — shares are NOT normalised within
the group. (Prior ~45% was a bug — the entity-year aggregation silently dropped ~562 GtCO₂e of
null-LEI emitters; fixed 2026-06-17, see `wiki/findings/2026-06-17-lei-dropna-fix.md`.)

**ERA5 CDS download note**: New CADS quota system (2024) rejects requests over ~10,000–15,000 time steps × grid area. For precipitation downloads use decade batches at 4x/day (00/06/12/18 UTC) — each batch ~7,440 fields, well within limits.

Immediate next steps:
- Verify AUD 10B central damage estimate for QLD floods (Deloitte/QLD Treasury/NEMA source)
- Add third event to test pipeline generalisability (now straightforward — `src/attribution` reusable)
- Quantify GEV distribution-form uncertainty (currently a single parametric fit per pool)
- CO₂e-consistent global denominator for the warming-share calculation (see emissions-to-forcing)
- Reinstate a reproducible producer for the QLD ERA5 wet-season α=0.289 (`ERA5_observed` row in `qld_amplification_factor.csv`) — currently an orphan value carried in the CSV and preserved by nb06's save cell; no notebook recomputes it (see `wiki/findings/2026-06-17-lei-dropna-fix.md`)
- Design web API layer for serving per-event liability tables
