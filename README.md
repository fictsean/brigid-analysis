# brigid-analysis

Climate attribution models that quantify the proportional liability of specific polluting entities (Carbon Majors, state actors) for specific climate disasters. The end goal is a web application that accepts a disaster as input and returns a structured liability breakdown with uncertainty ranges.

## What this does

The pipeline traverses a chain from named emitter to quantified liability:

```
Named Emitter → Cumulative Emissions → Atmospheric Forcing → Climate Signal → P(event) Change → Damages → Liability Fraction
```

Each step propagates uncertainty. Physical attribution (contribution to warming) is kept strictly separate from legal liability framing throughout.

## Current status

Five notebooks completed, with a full end-to-end pipeline proven on Black Summer 2019–20:

| Notebook | What it does | Key output |
|----------|-------------|------------|
| `01-exploration/02_carbon_majors_ingest` | Load & validate Carbon Majors DB (178 entities, 1854–2024) | `cm_entity_year.parquet`, `cm_cumulative_summary.parquet` |
| `02-attribution/01_emissions_to_warming` | FaIR v2.2 warming attribution per entity (841-config AR6 ensemble) | `entity_warming_contribution.parquet` |
| `02-attribution/02_australia_regional_amplification` | CMIP6 SE Australia amplification factor (hist, ACCESS models) | `au_amplification_factor.csv` |
| `02-attribution/03_black_summer_pr_cmip6` | CMIP6 hist vs hist-nat PR verification (null result — see below) | `black_summer_pr_cmip6.csv` |
| `03-liability/01_black_summer_liability` | End-to-end liability for Black Summer 2019–20 using WWA PR values | `black_summer_liability.parquet` |

**Black Summer headline result (central scenario):** USD 6.1B total Carbon Majors attributed liability — Saudi Aramco USD 521M, ExxonMobil USD 439M. Biggest uncertainty driver is the damage accounting approach (50× range from insured to total social cost), not the attribution science.

**Regional amplification:** CMIP6 models give SE Australia an amplification factor of 0.93× global mean warming. Observed BoM data implies ~1.35×, so model-based estimates are conservative lower bounds — consistent with the known underestimation bias acknowledged in the WWA Black Summer study.

**CMIP6 PR verification (null result):** Independent PR computation from CMIP6 hist vs hist-nat gave PR ≈ 0.6, opposite of physical expectation (WWA: PR ≥ 10). Root cause: the 4 models with hist-nat tasmax available on pangeo underestimate Australian warming and have unbalanced ensemble sizes. The WWA PR values remain authoritative. ERA5 observations are needed to anchor the factual distribution — next step.

## Setup

Requires Python 3.12+ and [uv](https://github.com/astral-sh/uv).

```bash
# Install uv (macOS)
brew install uv

# Create environment and install dependencies
uv sync

# Launch JupyterLab
.venv/bin/jupyter lab
```

The Jupyter kernel is registered as **"Brigid Analysis (Python 3.12)"**. Select it when opening any notebook.

## Repo layout

```
data/raw/           # never edited; gitignored for large files
data/processed/     # cleaned and joined outputs (parquet)
data/sources.md     # provenance log for every dataset
notebooks/
  01-exploration/   # data ingestion and validation
  02-attribution/   # emissions → warming via FaIR
  03-liability/     # event-level liability calculations
  99-scratch/       # throwaway work
src/                # Python modules extracted from notebooks
  attribution/
  data/
  models/
outputs/figures/    # saved plots (gitignored)
wiki/               # Obsidian vault — LLMwiki pattern
CLAUDE.md           # project context for AI-assisted sessions
```

## Wiki

The `wiki/` directory is an Obsidian vault using the LLMwiki pattern — pages are written to serve as LLM context as well as human documentation. Start at `wiki/CONTEXT.md`, navigate via `wiki/INDEX.md`.

Key sections: `datasets/`, `methods/`, `disasters/`, `findings/`.

## Key external resources

- Carbon Majors database: [carbonmajors.org](https://carbonmajors.org) — free download, T&C required
- WWA attribution studies: [worldweatherattribution.org](https://worldweatherattribution.org)
- CMIP6 via pangeo: [pangeo-forge.org](https://pangeo-forge.org)
- ERA5 reanalysis: [Copernicus CDS](https://cds.climate.copernicus.eu) — free account + `~/.cdsapirc` key required; needed to anchor factual temperature distribution for PR calculation
- EM-DAT disaster database: [emdat.be](https://emdat.be) — free academic registration required; needed for multi-event scaling
- CMIP6 catalog: cached at `data/processed/pangeo-cmip6.json` + `pangeo-cmip6.csv` (80MB, local copy avoids GCS catalog latency)
