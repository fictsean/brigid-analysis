# brigid-analysis

Climate attribution models that quantify the proportional liability of specific polluting entities (Carbon Majors, state actors) for specific climate disasters. The end goal is a web application that accepts a disaster as input and returns a structured liability breakdown with uncertainty ranges.

## What this does

The pipeline traverses a chain from named emitter to quantified liability:

```
Named Emitter → Cumulative Emissions → Atmospheric Forcing → Climate Signal → P(event) Change → Damages → Liability Fraction
```

Each step propagates uncertainty. Physical attribution (contribution to warming) is kept strictly separate from legal liability framing throughout.

## Current status

End-to-end pipeline proven on two events: **Black Summer 2019–20** and **2022 SE Queensland floods**.

### Black Summer 2019–20

| Notebook | What it does | Key output |
|----------|-------------|------------|
| `01-exploration/02_carbon_majors_ingest` | Load & validate Carbon Majors DB (178 entities, 1854–2024) | `cm_entity_year.parquet`, `cm_cumulative_summary.parquet` |
| `02-attribution/01_emissions_to_warming` | FaIR v2.2 warming attribution per entity (841-config AR6 ensemble) | `entity_warming_contribution.parquet` |
| `02-attribution/02_australia_regional_amplification` | CMIP6 SE Australia amplification factor (ACCESS-CM2, ACCESS-ESM1-5) | `au_amplification_factor.csv` |
| `02-attribution/03_black_summer_pr_cmip6` | CMIP6 hist vs hist-nat PR verification (null result — see below) | `black_summer_pr_cmip6.csv` |
| `02-attribution/04_black_summer_pr_era5` | Nonstationary GEV shift-fit PR (thin caller of `src/attribution`) | `black_summer_pr_shiftfit_bootstrap.parquet` |
| `02-attribution/05_observed_amplification` | ERA5 observed SE AU fire-season amplification (0.726, primary β) | `observed_amplification_factor.csv` |
| `03-liability/01_black_summer_liability` | End-to-end liability, global-share apportionment | `black_summer_liability.parquet` |

**Headline result:** GEV shift-fit PR=4.0 [2.4–15.4], FAR=0.752, central Carbon Majors liability **USD 3.92B** (AUD 10B direct damages). The primary PR sits exactly at the WWA FWI lower bound (PR≥4). Liability is apportioned by each entity's **global** warming share — Carbon Majors collectively cover **~75%** of global fossil CO₂ (close to the ~71% Heede figure), so absorb ~75% of climate-attributed damages. Damage accounting (~44× range from insured losses to total social cost) is the dominant uncertainty, not the attribution science.

**CMIP6 PR null result:** Independent CMIP6 hist vs hist-nat gave PR≈0.6 (wrong direction). Root cause: available hist-nat models underestimate Australian warming. The GEV shift-fit builds its counterfactual from the observed ERA5 record itself (no CMIP6 needed) and matches WWA; CMIP6 hist-nat is retained as a documented null-result reference only.

### 2022 SE Queensland Floods

| Notebook | What it does | Key output |
|----------|-------------|------------|
| `02-attribution/06_qld_floods_regional_amplification` | SE QLD warming amplification — CMIP6 median 0.882, ERA5 observed 0.289 | `qld_amplification_factor.csv` |
| `02-attribution/07_qld_floods_pr_era5` | ERA5 precip multiplicative GEV shift-fit (no WWA study exists) | `qld_floods_pr_shiftfit_bootstrap.parquet` |
| `03-liability/02_qld_floods_liability` | End-to-end liability, global-share apportionment | `qld_floods_liability.parquet` |

**Headline result:** Multiplicative GEV shift-fit PR=1.11 [1.05–1.30], FAR=0.101, central Carbon Majors liability **USD 0.53B** (AUD 10B damages, placeholder — needs verification). PR is a conservative lower bound: ERA5 wet-season land Tmax amplification (α=0.289) underestimates the SST-driven moisture forcing relevant to QLD flood extremes; the CMIP6 α=0.882 sensitivity gives PR=1.39, FAR=0.28.

**Methodological note:** Both events use a WWA-style **nonstationary GEV shift-fit** referenced to pre-industrial (`src/attribution/shift_fit.py`) — additive for Black Summer temperature, multiplicative (Clausius-Clapeyron) for QLD precipitation. See `wiki/findings/2026-06-13-methodology-revision.md` for the methodology revision that replaced the earlier Gaussian approaches.

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
