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
- **Citation**: Hersbach, H., Bell, B., Berrisford, P., et al. (2023): ERA5 monthly averaged data on single levels from 1940 to present. Copernicus Climate Change Service (C3S) Climate Data Store (CDS). DOI: 10.24381/cds.f17050d7
- **License**: [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). Contains modified Copernicus Climate Change Service information. Neither the European Commission nor ECMWF is responsible for any use that may be made of the Copernicus information or data it contains.
- **Attribution requirement**: Credit Copernicus C3S/ECMWF and link to CC BY 4.0 in any publication or product using this data or derivatives.
- **Notes**: Primary observed climate dataset. Use `cdsapi` Python client. API key in `~/.cdsapirc`. Downloaded subset: SE Australia monthly `maximum_2m_temperature`, Oct–Mar fire season months, 1961–2020.
- **Wiki**: [[era5-reanalysis]]
- **Status**: downloaded — `data/raw/era5/era5_mx2t_se_australia_1961_2020.nc`

---

## EM-DAT International Disaster Database
- **Source**: Centre for Research on the Epidemiology of Disasters (CRED), UCLouvain
- **URL**: https://www.emdat.be/
- **Coverage**: 1900–present; global natural and technological disasters
- **Format**: CSV (exported from query builder at emdat.be)
- **Raw path**: `data/raw/emdat/` (gitignored — no redistribution per Data Use Agreement)
- **Processed path**: `data/processed/emdat_disasters.parquet` (gitignored — same reason)
- **License**: EM-DAT Data Use Agreement — non-commercial, no redistribution
- **Citation**: EM-DAT: The Emergency Events Database — Université catholique de Louvain (UCL) — CRED, D. Guha-Sapir — www.emdat.be, Brussels, Belgium.
- **Notes**: Damage values are nominal USD; CPI-adjusted to 2020 USD in ingest notebook using BLS CPI-U. Disaster Group = Natural filter applied. `'000 US$` fields multiplied by 1000.
- **Wiki**: [[datasets/emdat]]
- **Status**: not yet downloaded — register at emdat.be to obtain

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
