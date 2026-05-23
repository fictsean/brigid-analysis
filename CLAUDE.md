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

## Completed Work (as of 2026-05-23)

### Data
- `data/raw/carbon_majors/emissions_high_granularity.csv` — downloaded, 178 entities 1854–2024
- CMIP6 — streamed on demand from pangeo zarr (no local download needed)
- EM-DAT, ERA5 — not yet downloaded

### Notebooks
1. `01-exploration/01_environment_check.ipynb` — verifies all packages and pangeo connectivity
2. `01-exploration/02_carbon_majors_ingest.ipynb` — loads Carbon Majors, produces entity-year and cumulative summary parquets
3. `02-attribution/01_emissions_to_warming.ipynb` — FaIR v2.2 warming attribution, 841-config AR6 posterior ensemble
4. `02-attribution/02_australia_regional_amplification.ipynb` — CMIP6 historical SE AU amplification factor; ACCESS-CM2 + ACCESS-ESM1-5
5. `02-attribution/03_black_summer_pr_cmip6.ipynb` — independent PR computation from CMIP6 hist vs hist-nat; BCC-CSM2-MR, GFDL-ESM4, IPSL-CM6A-LR, MRI-ESM2-0 (in progress)
6. `03-liability/01_black_summer_liability.ipynb` — first end-to-end chain; Black Summer 2019–20

### Key processed files
- `data/processed/cm_entity_year.parquet` — entity × year emissions
- `data/processed/cm_cumulative_summary.parquet` — cumulative totals and global share per entity
- `data/processed/entity_warming_contribution.parquet` — per-entity warming (p05/p50/p95) + warming_au_* columns
- `data/processed/fair_global_temperature.parquet` — FaIR ensemble temperature timeseries
- `data/processed/au_amplification_factor.csv` — per-model SE AU amplification; ensemble median 0.935
- `data/processed/black_summer_liability.parquet` — entity liability estimates (WWA PR scenarios + au_warming_share + liability_au_* columns)
- `data/processed/black_summer_pr_cmip6.csv` — CMIP6-derived PR at multiple thresholds (PR=0.6, null result — do not use for liability)
- `data/processed/black_summer_pr_bootstrap.parquet` — 2,000-iteration bootstrap samples (PR range 0.5–0.7)

### Wiki findings
- `wiki/findings/2026-05-15-carbon-majors-ingest.md`
- `wiki/findings/2026-05-15-emissions-to-warming.md`
- `wiki/findings/2026-05-18-black-summer-liability.md`
- `wiki/findings/2026-05-23-australia-regional-amplification.md` — CMIP6 SE AU amplification 0.935; models underestimate observed (~1.35); liability estimates are conservative lower bounds
- `wiki/findings/2026-05-24-black-summer-pr-cmip6.md` — CMIP6 PR verification null result (PR=0.6); available hist-nat model subset does not reproduce AU warming signal; WWA PR values stand

## Current Status / Next Steps

End-to-end pipeline proven on Black Summer 2019–20 (central result: USD 6.1B Carbon Majors liability). Regional amplification factor computed and incorporated. Independent CMIP6 PR computation underway.

Immediate next steps:
- Add BoM observed amplification (~1.35) as additional scenario in Black Summer liability notebook
- Register for EM-DAT to enable multi-event scaling
- Design web API layer for serving per-event liability tables
