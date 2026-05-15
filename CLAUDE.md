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

- Carbon Majors database: climateaccountability.org
- WWA studies: worldweatherattribution.org
- CMIP6 data: ESGF nodes or pangeo-forge.org
- ERA5 reanalysis: Copernicus Climate Data Store (CDS)
- Disaster records: EM-DAT (emdat.be) — requires free academic registration
- Key paper: Ekwurzel et al. (2017) "The rise in global atmospheric CO2, surface temperature, and sea level from emissions traced to major carbon producers"

## Conventions

- Notebooks are numbered and named: `01-exploration/01_carbon_majors_ingest.ipynb`
- Every notebook that produces a meaningful result gets a corresponding `wiki/findings/YYYY-MM-DD-slug.md` page
- All uncertainty estimates are expressed as 5th–95th percentile ranges unless stated otherwise
- Physical attribution (contribution to risk) is kept strictly separate from legal liability framing

## Current Status

Project initialized 2026-05-14. No notebooks yet. Next step: ingest Carbon Majors emissions data, ERA5 temperature anomalies, and EM-DAT disaster records as the foundation for the first attribution pipeline.
