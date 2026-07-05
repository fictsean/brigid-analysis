---
type: dataset
name: emdat
tags: [disasters, damages, deaths, foundational]
related: [era5-reanalysis, wwa-studies, methods/attribution-chain]
status: active
confidence: high
last_updated: 2026-07-05
---

# EM-DAT International Disaster Database

Maintained by the Centre for Research on the Epidemiology of Disasters (CRED) at UCLouvain.
Comprehensive global record of natural and technological disasters from 1900 to present.

## Role in This Project

EM-DAT provides the **damage estimate** input to the liability formula:

```
entity_liability = entity_warming_share × FAR × total_damages
```

It is the authoritative source for `total_damages` at scale — replacing per-event manual research
as the pipeline is applied to multiple disasters.

Field mapping to our damage scenarios:

| EM-DAT field | Scenario |
|---|---|
| `Insured Damage` | Conservative (insured losses only) |
| `Total Damage` | Central (direct economic losses) |
| *(no analog)* | Comprehensive (total social cost — stays per-event hardcoded) |

## License and Attribution

Data obtained under the [EM-DAT Terms of Use](https://doc.emdat.be/docs/legal/terms-of-use/)
(verified 2026-07-05). Access is free but **conditional and restricted** — it is *not* an open
(CC-BY) licence. Authorised users are academic/research institutions, international public
organisations, national governments, and media agencies, for research/teaching/information purposes.

**Prohibitions (quoted from the Terms of Use)** — users shall not:
1. "Reproduce, copy, communicate, lend, or otherwise distribute EM-DAT or a substantial part of EM-DAT";
2. "Share, use or transmit any portion of EM-DAT via the Internet to unauthorized users";
3. "Create substitute or derivative databases of EM-DAT";
4. Make any **commercial** use of EM-DAT (including its data and derivative products) except under a
   separate paid Database License Agreement.

**Citation** ([Citation Policy](https://doc.emdat.be/docs/legal/citation-policy/)):
> EM-DAT, CRED / UCLouvain, Brussels, Belgium — www.emdat.be

### ⚠️ Implication for the public web app (verified 2026-07-05)

**EM-DAT-derived figures must NOT be surfaced in the public explorer app.** Publishing them would
(a) "transmit … EM-DAT via the Internet to unauthorized users" (the general public are not
authorised users), and (b) risk the JSON catalog being a prohibited "derivative database". The
non-commercial clause is a further constraint if brigid.earth is ever monetised.

**Resolution — no pipeline change needed.** The pipeline already treats EM-DAT as an *internal
validation cross-check only*; the primary `total_damages` inputs are independently-sourced
ICA/Deloitte/government figures (see [[disasters/qld-floods-2022]], [[disasters/black-summer-2019-20]]).
Guardrail for `scripts/export_web_catalog.py` (Phase 2): the exporter must read damage figures from
the independently-sourced event specs, never from `emdat_disasters.parquet`.

**Compliance**: Raw data (`data/raw/emdat/`) and the processed parquet
(`data/processed/emdat_disasters.parquet`) are both excluded from version control.
Anyone cloning the repo must register and download independently.

## Key Facts

- Coverage: 1900–present; ~26,000 disaster entries
- Scope: natural disasters (meteorological, hydrological, climatological, geophysical, biological)
  and technological
- Key metrics: deaths, injured, affected, total damages (USD nominal), insured losses (USD)
- Damage values are **nominal USD** — inflation-adjust before cross-year comparisons (our ingest
  notebook CPI-adjusts to 2020 USD using BLS CPI-U)
- Updated continuously; export date affects which events are included

## Access

- Registration: free academic account at emdat.be (approval typically 1–2 days)
- Download: query builder → export CSV, Disaster Group = Natural, all countries, 1900–present
- Local raw path: `data/raw/emdat/` (gitignored)
- Processed parquet: `data/processed/emdat_disasters.parquet` (gitignored)

## Key Variables (processed column names)

| Column | Description |
|--------|-------------|
| `dis_no` | Unique disaster ID (e.g. `2019-0546-AUS`) |
| `disaster_type` | e.g. Wildfire, Flood, Storm, Drought |
| `disaster_subtype` | e.g. Forest fire, Flash flood |
| `country` | Country name |
| `country_iso3` | ISO3 code (e.g. `AUS`) |
| `start_year`, `start_month`, `start_day` | Event start date |
| `end_year`, `end_month`, `end_day` | Event end date |
| `event_name` | Optional name (e.g. `Black Summer`) |
| `total_deaths` | Direct mortality |
| `total_affected` | Deaths + injured + affected |
| `total_damage_usd` | Total economic losses (full USD, nominal) |
| `insured_damage_usd` | Insured losses (full USD, nominal) |
| `total_damage_usd_2020` | CPI-adjusted to 2020 USD |

## Ingest Notebook

`notebooks/01-exploration/03_emdat_ingest.ipynb` — loads raw CSV, normalises columns across
export versions, converts `'000 US$` fields to full USD, applies CPI adjustment, saves parquet,
and validates against the Black Summer hardcoded scenarios.

## Caveats

- Damage coverage is incomplete: many events, especially in low-income countries, have no damage
  figure recorded. Nulls are common.
- Classification changed over time — `Disaster Type = Wildfire` may appear as `Forest fire` in
  older records. The ingest notebook uses a fuzzy match.
- Nominal USD values need CPI adjustment for cross-year comparisons. Our CPI table covers
  1990–2023 (BLS CPI-U, hardcoded). Events before 1990 use the nominal value.
- EM-DAT records direct economic losses, not total social cost. The comprehensive damage scenario
  (health costs, smoke mortality, ecosystem services) requires separate academic sources.

## Related

- [[methods/attribution-chain]] — where damage estimates enter the liability formula
- [[methods/far-probability-ratio]] — FAR applied to EM-DAT damages to partition climate-attributed share
- [[wwa-studies]] — richer event-level data for specific disasters
- [[disasters/black-summer-2019-20]] — first event validated against EM-DAT
