---
type: context
last_updated: 2026-05-28
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

**Phase 4 — Multi-Event Pipeline** (active)

End-to-end attribution pipeline proven on two events. A WWA-style **nonstationary GEV shift-fit**
(`src/attribution/shift_fit.py`) is the primary PR method across both events; liability is apportioned
by each entity's **global** warming share. See [[findings/2026-06-13-methodology-revision]] for the
methodology revision that established both.

Completed:
- Full Carbon Majors ingestion (1,435 GtCO₂e, 178 entities, 1854–2024)
- FaIR v2.2 emissions-to-warming attribution (841-config AR6 posterior ensemble)
- SE Australia regional amplification — CMIP6 annual-tas median 0.935; ERA5 fire-season 0.726 (primary β)
- **Black Summer 2019–20**: GEV shift-fit PR=4.0 [2.4–15.4], FAR=0.752, central Carbon Majors liability USD 3.92B (matches WWA FWI lower bound)
- CMIP6 hist vs hist-nat PR verification — null result (PR=0.6); retained as reference only
- EM-DAT ingestion for programmatic damage lookup (17,849 records); Black Summer fragmented so hardcoded PBO/ICA scenarios remain primary
- SE QLD regional amplification — CMIP6 annual-tas median 0.882; ERA5 wet-season Tmax 0.289 (primary β, conservative)
- **2022 SE QLD Floods**: multiplicative GEV shift-fit PR=1.11 [1.05–1.30], FAR=0.101, central Carbon Majors liability USD 0.53B (AUD 10B placeholder damages)

Pending:
- Verify AUD 10B central damage estimate for QLD floods (QLD Treasury / Deloitte / NEMA)
- Add third event to test pipeline generalisability (src/attribution is reusable)
- Quantify GEV distribution-form uncertainty; CO₂e-consistent warming-share denominator
- Web API layer for per-event liability tables

## Wiki Navigation

- [[INDEX]] — full page manifest
- [[entities/]] — Carbon Majors companies and state actors
- [[disasters/]] — specific climate events
- [[datasets/]] — data source documentation
- [[methods/]] — attribution methodologies
- [[findings/]] — dated research conclusions
- [[concepts/]] — scientific, legal, economic terms
- [[models/]] — ML/statistical models built
