---
type: dataset
name: cmip6
tags: [climate-models, counterfactual, scenarios]
related: [era5-reanalysis, methods/far-probability-ratio, 2026-05-23-australia-regional-amplification, 2026-05-24-black-summer-pr-cmip6]
status: active
confidence: medium
last_updated: 2026-05-24
---

# CMIP6 Climate Model Outputs

Coupled Model Intercomparison Project Phase 6. A coordinated ensemble of global climate model runs used to understand past climate and project future change. Primary use here: constructing counterfactual (natural-forcing-only) climates for attribution.

## Key Facts

- ~100 models from ~50 modeling centers worldwide
- Historical runs: 1850–2014 (with anthropogenic + natural forcing)
- Counterfactual runs: `hist-nat` experiment (natural forcing only, no human emissions)
- Future scenarios: SSP1-1.9 through SSP5-8.5 (2015–2100)

## Access

**Option 1 — pangeo (recommended for cloud):**
- Zarr stores accessible via `intake-esm`
- Catalog: https://storage.googleapis.com/cmip6/pangeo-cmip6.json
- No download required; stream data directly

**Option 2 — ESGF:**
- Node: esgf-node.llnl.gov
- Download via `esgf-pyclient` or web interface
- Local path: `data/raw/cmip6/` (gitignored — files are very large)

## Key Variables for This Project

| Variable | CMIP6 name | Use |
|----------|-----------|-----|
| Surface air temperature | `tas` | Warming attribution |
| Precipitation | `pr` | Flood/drought attribution |
| Max daily temperature | `tasmax` | Heat wave attribution |
| Sea surface temperature | `tos` | Hurricane intensification |

## Key Experiments

| Experiment | Description |
|-----------|-------------|
| `historical` | All forcings (factual past climate) |
| `hist-nat` | Natural forcing only (counterfactual — no human emissions) |
| `piControl` | Pre-industrial control (no trend baseline) |

## Local Catalog Cache

The pangeo catalog JSON + CSV (80MB) is cached locally at `data/processed/pangeo-cmip6.json` and `data/processed/pangeo-cmip6.csv`. Load via:
```python
col = intake.open_esm_datastore('data/processed/pangeo-cmip6.json')
```
This avoids the slow GCS catalog fetch on every run.

## Australian Regional Caveats

CMIP6 models **underestimate SE Australian warming** — ensemble amplification (SE AU / global) is 0.93 in CMIP6 vs ~1.35 observed (BoM). This is documented in [[2026-05-23-australia-regional-amplification]].

For PR calculation, only 4 models have both `historical` and `hist-nat` `tasmax` on pangeo (BCC-CSM2-MR, GFDL-ESM4, IPSL-CM6A-LR, MRI-ESM2-0). These models produce PR ≈ 0.6 for SE Australian heat — a null result that reflects model underestimation, not physical reality. ERA5 is needed to anchor the factual distribution. See [[2026-05-24-black-summer-pr-cmip6]].

## General Caveats

- Use multi-model ensembles (10+ models) to characterize structural uncertainty
- Models have different climate sensitivities — report spread, not just ensemble mean
- `hist-nat` runs are not available for all models; available subset is non-representative for Australia

## Related

- [[era5-reanalysis]] — observed counterpart; use for bias correction
- [[methods/far-probability-ratio]] — counterfactual vs. factual comparison methodology
