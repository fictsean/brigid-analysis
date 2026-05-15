---
type: dataset
name: era5-reanalysis
tags: [climate, observed, temperature, precipitation]
related: [cmip6, carbon-majors-database]
status: stub
confidence: high
last_updated: 2026-05-14
---

# ERA5 Reanalysis

ECMWF's fifth-generation atmospheric reanalysis. Combines model data with observations to produce a globally consistent climate record from 1940 to near-present. Primary source for observed climate variables.

## Key Facts

- Temporal coverage: 1940–present (near real-time updates)
- Spatial resolution: ~31km (~0.25°)
- Temporal resolution: hourly
- Variables: 2m temperature, precipitation, wind, humidity, sea surface temperature, and hundreds more

## Access

- API: Copernicus Climate Data Store (CDS) — requires free account at cds.climate.copernicus.eu
- Python client: `cdsapi`
- API key location: `~/.cdsapirc`
- Local path: `data/raw/era5/` (gitignored — files are large NetCDF)

## Typical Usage in This Project

- Observed temperature anomalies for validating climate signal step
- Extreme event characterization (heat wave intensity, precipitation totals)
- Reference climatology for return period calculations

## Caveats

- Files are large (.nc format); download only the variables and regions needed
- Pre-1950 data has lower quality due to sparse observations
- Use `xarray` + `cfgrib` or `netCDF4` for reading

## Related

- [[cmip6]] — model outputs; ERA5 is the observed counterpart
- [[methods/far-probability-ratio]] — ERA5 used for factual climate characterization
