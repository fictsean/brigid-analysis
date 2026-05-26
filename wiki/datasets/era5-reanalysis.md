---
type: dataset
name: era5-reanalysis
tags: [climate, observed, temperature, precipitation]
related: [cmip6, carbon-majors-database, methods/far-probability-ratio]
status: stub
confidence: high
last_updated: 2026-05-24
license: CC BY 4.0
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

- **P1 (factual distribution)** for PR calculation — ERA5 anchors the factual temperature distribution to observed reality, avoiding the CMIP6 historical underestimation bias (see [[datasets/cmip6]])
- Extreme event characterization (heat wave intensity, fire weather indices)
- Reference climatology for return period calculations

## Why ERA5 Over CMIP6 Historical for P1

CMIP6 historical runs underestimate SE Australian warming (~0.93× amplification vs observed ~1.35×). Using CMIP6 historical for the factual distribution gives a factual world that is too cool, which suppresses the PR signal. ERA5 is the observed record — using it for P1 replicates the WWA methodology and avoids this bias. See [[2026-05-24-black-summer-pr-cmip6]].

## License and Attribution

ERA5 is provided under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). Any use of ERA5 data or derivatives must:

1. **Credit** Copernicus Climate Change Service (C3S) / ECMWF
2. **Cite**: Hersbach et al. (2023), DOI: 10.24381/cds.f17050d7
3. **Include disclaimer**: "Contains modified Copernicus Climate Change Service information. Neither the European Commission nor ECMWF is responsible for any use that may be made of the Copernicus information or data it contains."
4. **Link to the license**: https://creativecommons.org/licenses/by/4.0/

This applies to figures, reports, web applications, and any other outputs that incorporate ERA5 data or statistics derived from it.

## Access Setup

CDS API key configured in `~/.cdsapirc`. To set up on a new machine:
1. Register free at https://cds.climate.copernicus.eu
2. Accept dataset licence at the CDS dataset page before first download
3. Add `~/.cdsapirc`:
   ```
   url: https://cds.climate.copernicus.eu/api
   key: YOUR-KEY-HERE
   ```
4. Download targeted regional subsets — do not download global files

## ARCO-ERA5 (Pangeo Alternative)

Google Cloud hosts ERA5 as zarr at `gcp-public-data-arco-era5/`. However, the hourly zarr is chunked 1 timestep × full global grid — unusable for time-series streaming. The CDS API targeted download is strongly preferred.

## Caveats

- Files are large (.nc format); always subset to the region and variables needed
- Pre-1950 data has lower quality due to sparse observations
- `maximum_2m_temperature` (mx2t) is available as monthly mean of daily max — equivalent to CMIP6 `tasmax`

## Related

- [[cmip6]] — model outputs; ERA5 is the observed counterpart
- [[methods/far-probability-ratio]] — ERA5 used for factual climate characterization
