---
type: context
last_updated: 2026-05-14
---

# Brigid Analysis — Project Context

## Mission

Build climate attribution models that quantify the proportional liability of specific polluting entities (Carbon Majors, state actors) with respect to specific climate disasters. End goal: a web application that takes a disaster as input and returns a structured liability breakdown with uncertainty ranges.

## The Attribution Chain

```
Named Emitter → Cumulative Emissions → Atmospheric Forcing → Climate Signal → P(event) Change → Damages → Liability Fraction
```

Each step is quantified with 5–95th percentile uncertainty ranges. Physical attribution (contribution to warming) is kept separate from legal liability framing.

## Key Concepts

- **Fraction of Attributable Risk (FAR)**: fraction of event probability attributable to climate change. FAR = 1 - (P0/P1) where P0 is probability in counterfactual climate, P1 in factual.
- **Probability Ratio (PR)**: P1/P0 — how many times more likely an event is with climate change vs. without.
- **Carbon Majors**: ~100 fossil fuel producers responsible for ~71% of global industrial GHG emissions since 1854 (Heede 2014).
- **Counterfactual climate**: modeled climate without anthropogenic forcing, used as the baseline for attribution.

## Primary Data Sources

| Source | What it provides | Wiki page |
|--------|-----------------|-----------|
| Carbon Majors Database | Emissions by company-year, 1854–present | [[carbon-majors-database]] |
| ERA5 Reanalysis | Observed climate, 1940–present | [[era5-reanalysis]] |
| EM-DAT | Disaster records with damages, 1900–present | [[emdat]] |
| CMIP6 | Climate model ensembles for counterfactuals | [[cmip6]] |
| WWA Studies | Pre-computed FAR/PR for specific events | [[wwa-studies]] |

## Current Research Phase

**Phase 1 — Data Ingestion & Exploration** (active)

Ingest and validate Carbon Majors, ERA5, and EM-DAT as the foundation for the first attribution pipeline. No results yet.

## Wiki Navigation

- [[INDEX]] — full page manifest
- [[entities/]] — Carbon Majors companies and state actors
- [[disasters/]] — specific climate events
- [[datasets/]] — data source documentation
- [[methods/]] — attribution methodologies
- [[findings/]] — dated research conclusions
- [[concepts/]] — scientific, legal, economic terms
- [[models/]] — ML/statistical models built
