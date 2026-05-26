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
- Disaster records: EM-DAT (emdat.be) — free academic registration required, not yet downloaded
- Key paper: Ekwurzel et al. (2017) "The rise in global atmospheric CO2, surface temperature, and sea level from emissions traced to major carbon producers"
- FaIR model: https://github.com/OMS-NetZero/FAIR — v2.2 with fair-calibrate v1.4 posterior (841 configs)

## Conventions

- Notebooks are numbered and named: `01-exploration/02_carbon_majors_ingest.ipynb`
- Every notebook that produces a meaningful result gets a corresponding `wiki/findings/YYYY-MM-DD-slug.md` page
- All uncertainty estimates are expressed as 5th–95th percentile ranges unless stated otherwise
- Physical attribution (contribution to risk) is kept strictly separate from legal liability framing
- Processed data saved as parquet; figures saved to `outputs/figures/` (gitignored)

## Completed Work (as of 2026-05-24)

### Data
- `data/raw/carbon_majors/emissions_high_granularity.csv` — downloaded, 178 entities 1854–2024
- CMIP6 — streamed on demand from pangeo zarr (no local download needed)
- ERA5 daily mx2t — downloaded, `data/raw/era5/era5_mx2t_daily_se_australia_1961_2020.nc` (83 MB, gitignored)
- EM-DAT — not yet downloaded

### Notebooks
1. `01-exploration/01_environment_check.ipynb` — verifies all packages and pangeo connectivity
2. `01-exploration/02_carbon_majors_ingest.ipynb` — loads Carbon Majors, produces entity-year and cumulative summary parquets
3. `02-attribution/01_emissions_to_warming.ipynb` — FaIR v2.2 warming attribution, 841-config AR6 posterior ensemble
4. `02-attribution/02_australia_regional_amplification.ipynb` — CMIP6 historical SE AU amplification factor; ACCESS-CM2 + ACCESS-ESM1-5
5. `02-attribution/03_black_summer_pr_cmip6.ipynb` — independent PR computation from CMIP6 hist vs hist-nat; null result PR=0.6; do not use for liability
6. `02-attribution/04_black_summer_pr_era5.ipynb` — ERA5 daily mx2t + CMIP6 hist-nat bootstrap (4 models, cftime bug fixed); PR=1.8 [1.0–2.9] median; 3.3 at 99th pct; **primary PR source**
7. `02-attribution/05_observed_amplification.ipynb` — ERA5 observed SE AU fire-season amplification = 0.726; CMIP6 = 0.935; obs-corrected liability 1.96B
8. `03-liability/01_black_summer_liability.ipynb` — first end-to-end chain; Black Summer 2019–20; ERA5 bootstrap central liability USD 3.07B

### Key processed files
- `data/processed/cm_entity_year.parquet` — entity × year emissions
- `data/processed/cm_cumulative_summary.parquet` — cumulative totals and global share per entity
- `data/processed/entity_warming_contribution.parquet` — per-entity warming (p05/p50/p95) + warming_au_* columns
- `data/processed/fair_global_temperature.parquet` — FaIR ensemble temperature timeseries
- `data/processed/au_amplification_factor.csv` — per-model SE AU amplification: ACCESS-CM2 1.030, ACCESS-ESM1-5 0.841, ensemble median 0.935, ERA5_observed 0.726
- `data/processed/black_summer_liability.parquet` — entity liability estimates; columns: conservative/central/comprehensive + obs_p05/med/p95
- `data/processed/black_summer_pr_cmip6.csv` — CMIP6-derived PR at multiple thresholds (PR=0.6, null result — do not use for liability)
- `data/processed/black_summer_pr_bootstrap.parquet` — 2,000-iteration bootstrap samples (PR range 0.5–0.7, CMIP6 null result)
- `data/processed/black_summer_pr_era5.csv` — ERA5 daily mx2t + hist-nat PR at 4 thresholds (median 1.80; 99th pct 3.27; 4-model corrected run)
- `data/processed/black_summer_pr_era5_bootstrap.parquet` — 2,000-iteration ERA5 bootstrap samples (PR median 1.80)
- `data/processed/observed_amplification_factor.csv` — ERA5 observed amplification with trend metadata
- `data/raw/era5/era5_mx2t_daily_se_australia_1961_2020.nc` — ERA5 daily mx2t, 83 MB, gitignored

### Wiki findings
- `wiki/findings/2026-05-15-carbon-majors-ingest.md`
- `wiki/findings/2026-05-15-emissions-to-warming.md`
- `wiki/findings/2026-05-18-black-summer-liability.md`
- `wiki/findings/2026-05-23-australia-regional-amplification.md` — CMIP6 SE AU amplification 0.935 (ACCESS-CM2, ACCESS-ESM1-5)
- `wiki/findings/2026-05-24-black-summer-pr-cmip6.md` — CMIP6 PR verification null result (PR=0.6); available hist-nat model subset does not reproduce AU warming signal; WWA PR values stand
- `wiki/findings/2026-05-24-black-summer-pr-era5.md` — ERA5 daily mx2t + hist-nat (4 models, cftime bug fixed): PR=1.8 [1.0–2.9] median; 3.3 at 99th pct; USD 3.07B CM liability
- `wiki/findings/2026-05-24-observed-amplification.md` — ERA5 fire-season amplification = 0.726 (< CMIP6 0.935); obs-corrected liability 1.96B; ERA5 bootstrap 3.07B is primary

## Current Status / Next Steps

End-to-end pipeline proven on Black Summer 2019–20. ERA5 PR (median 1.80 [1.0–2.9]) is the primary source; WWA is validation only. Central liability: USD 3.07B (ERA5 bootstrap median). Note: a cftime calendar bug previously excluded GFDL-ESM4 and BCC-CSM2-MR from the P0 pool; the corrected 4-model run gives a lower PR (1.8 vs 2.7) due to wider natural-variability spread. Observed SE AU fire-season amplification (0.726) is lower than CMIP6 (0.935), so the obs-corrected scenario (1.96B) is a sensitivity lower bound.

Immediate next steps:
- Register for EM-DAT to enable multi-event scaling
- Design web API layer for serving per-event liability tables
- Apply pipeline to a second event
