---
type: dataset
name: carbon-majors-database
tags: [emissions, entities, foundational]
related: [era5-reanalysis, emdat, ekwurzel-2017, 2026-05-15-carbon-majors-ingest]
status: active
confidence: high
last_updated: 2026-05-24
---

# Carbon Majors Database

Traces historical fossil fuel and cement production — and associated CO2/CH4 emissions — to ~100 named investor-owned, state-owned, and nation-state producers from 1854 to the present. Foundational dataset for the entity → emissions step of the attribution chain.

## Key Facts

- ~71% of global industrial GHG emissions since 1854 traceable to named entities in this database
- Covers oil, gas, coal, and cement producers
- Includes both scope 1 (operational) and scope 3 (end-use combustion) emissions
- Updated periodically by Climate Accountability Institute; original methodology: Heede (2014)

## Access

- Download: https://climateaccountability.org/carbonmajors.html
- Local path: `data/raw/carbon_majors/`
- Format: CSV / Excel

## Key Variables

| Variable | Description |
|----------|-------------|
| `entity` | Producer name |
| `entity_type` | investor-owned / state-owned / nation-state |
| `commodity` | oil / gas / coal / cement |
| `year` | Production year |
| `production_value` | Production quantity |
| `production_unit` | Units (e.g., million barrels) |
| `total_emissions_MtCO2e` | Total GHG emissions in MtCO2e |

## Caveats

- Pre-1950 data has higher uncertainty
- Does not include land-use emissions
- Scope 3 attribution is contested legally — distinguish from scope 1/2 in liability calculations

## Related

- [[ekwurzel-2017]] — used this database to trace warming and sea level rise to named producers
- [[methods/emissions-to-forcing]] — how to go from company emissions to atmospheric forcing
