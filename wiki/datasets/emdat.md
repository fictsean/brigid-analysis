---
type: dataset
name: emdat
tags: [disasters, damages, deaths, foundational]
related: [era5-reanalysis, wwa-studies]
status: stub
confidence: high
last_updated: 2026-05-14
---

# EM-DAT International Disaster Database

Maintained by the Centre for Research on the Epidemiology of Disasters (CRED) at UCLouvain. Comprehensive global record of natural and technological disasters from 1900 to present.

## Key Facts

- Coverage: 1900–present; ~26,000 disaster entries
- Scope: natural disasters (meteorological, hydrological, climatological, geophysical, biological) and technological
- Key metrics: deaths, injured, affected, homeless, total damages (USD), insured losses (USD)
- Updated continuously

## Access

- Registration: free academic account at emdat.be
- Download: custom query builder on the website (CSV export)
- Local path: `data/raw/emdat/`
- Format: Excel or CSV

## Key Variables

| Variable | Description |
|----------|-------------|
| `Dis No` | Unique disaster ID |
| `Disaster Type` | e.g., Flood, Storm, Extreme temperature |
| `Disaster Subtype` | e.g., Tropical cyclone, Flash flood |
| `Country` | ISO country code |
| `Start Date` / `End Date` | Event dates |
| `Total Deaths` | Direct mortality |
| `Total Affected` | Deaths + injured + affected |
| `Total Damages ('000 US$)` | Economic losses (nominal) |

## Caveats

- Damage values are **nominal USD** — must inflation-adjust for cross-year comparisons
- Coverage is incomplete for smaller/older events and low-income countries
- Disaster classification changed over time — filter by `Disaster Group = Natural` for climate work
- Does not distinguish climate-attributable vs. non-climate damages — that's our job

## Related

- [[methods/far-probability-ratio]] — FAR applied to EM-DAT events to partition damages
- [[wwa-studies]] — richer event-level data for specific disasters
