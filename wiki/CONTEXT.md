---
type: context
last_updated: 2026-05-23
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

**Phase 3 — Attribution Pipeline Refinement** (active)

End-to-end liability pipeline proven on Black Summer 2019–20 (central result: USD 6.1B Carbon Majors liability). Now tightening the global→regional warming link and replacing borrowed WWA PR values with independently computed CMIP6 estimates.

Completed:
- Full Carbon Majors ingestion (1,435 GtCO₂e, 178 entities, 1854–2024)
- FaIR v2.2 emissions-to-warming attribution (841-config AR6 posterior ensemble)
- SE Australia regional amplification from CMIP6 historical (ensemble median 0.935; models underestimate observed ~1.35 — estimates are conservative lower bounds)
- End-to-end Black Summer liability pipeline (WWA-borrowed PR; three damage scenarios)

In progress:
- Independent PR computation from CMIP6 hist vs hist-nat tasmax (4 models, 19 member-runs, 2000-iteration bootstrap)

Pending:
- EM-DAT ingestion for multi-event scaling
- ERA5 regional trend verification
- Web API layer

## Wiki Navigation

- [[INDEX]] — full page manifest
- [[entities/]] — Carbon Majors companies and state actors
- [[disasters/]] — specific climate events
- [[datasets/]] — data source documentation
- [[methods/]] — attribution methodologies
- [[findings/]] — dated research conclusions
- [[concepts/]] — scientific, legal, economic terms
- [[models/]] — ML/statistical models built
