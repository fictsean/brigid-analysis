# Data Sources

Provenance log for all datasets used in this project. One entry per source.

---

## Carbon Majors Database
- **Source**: Climate Accountability Institute / Richard Heede
- **URL**: https://climateaccountability.org/carbonmajors.html
- **Coverage**: 1854–present; ~100 major fossil fuel producers
- **Format**: CSV / Excel
- **Raw path**: `data/raw/carbon_majors/`
- **Notes**: Traces ~71% of global industrial GHG emissions to named entities. Key variable is cumulative CO2e by company-year. Heede (2014) is the foundational paper; dataset updated periodically.
- **Wiki**: [[carbon-majors-database]]
- **Status**: not yet downloaded

---

## ERA5 Reanalysis
- **Source**: ECMWF via Copernicus Climate Data Store
- **URL**: https://cds.climate.copernicus.eu/
- **Coverage**: 1940–present; global; hourly at ~31km resolution
- **Format**: NetCDF (.nc) — large files, gitignored
- **Raw path**: `data/raw/era5/`
- **Notes**: Primary observed climate dataset. Use `cdsapi` Python client. Requires free CDS account and API key in `~/.cdsapirc`.
- **Wiki**: [[era5-reanalysis]]
- **Status**: not yet downloaded

---

## EM-DAT International Disaster Database
- **Source**: Centre for Research on the Epidemiology of Disasters (CRED), UCLouvain
- **URL**: https://www.emdat.be/
- **Coverage**: 1900–present; global natural and technological disasters
- **Format**: Excel / CSV (exported from web interface)
- **Raw path**: `data/raw/emdat/`
- **Notes**: Requires free academic registration. Key fields: disaster type, country, start/end date, total deaths, total damages (USD). Currency values are nominal; inflation-adjust before use.
- **Wiki**: [[emdat]]
- **Status**: not yet downloaded

---

## CMIP6 Climate Model Outputs
- **Source**: ESGF nodes / pangeo-forge
- **URL**: https://pangeo-forge.org / https://esgf-node.llnl.gov/
- **Coverage**: Historical (1850–2014) + SSP scenarios (2015–2100)
- **Format**: Zarr (pangeo) or NetCDF (ESGF) — very large, gitignored
- **Raw path**: `data/raw/cmip6/`
- **Notes**: Used for counterfactual (no-anthropogenic-forcing) vs. factual comparisons. Access via `intake-esm` or direct zarr store URLs. Focus on surface temperature (`tas`) and precipitation (`pr`) variables initially.
- **Wiki**: [[cmip6]]
- **Status**: not yet downloaded

---

## World Weather Attribution Studies
- **Source**: worldweatherattribution.org
- **Coverage**: Ad hoc; individual extreme events since ~2015
- **Format**: PDF reports + supplementary data
- **Raw path**: `data/raw/wwa/`
- **Notes**: Pre-computed FAR and PR values for specific events. Use as validation targets and methodological reference. Not a machine-readable database — extract key values manually into wiki/disasters/ pages.
- **Wiki**: [[wwa-studies]]
- **Status**: not yet downloaded
