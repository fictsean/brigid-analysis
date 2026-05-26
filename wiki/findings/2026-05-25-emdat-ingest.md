---
type: finding
name: 2026-05-25-emdat-ingest
tags: [emdat, damages, disasters, data-ingest]
related: [emdat, disasters/black-summer-2019-20, 2026-05-18-black-summer-liability]
status: active
confidence: high
last_updated: 2026-05-26
notebook: notebooks/01-exploration/03_emdat_ingest.ipynb
---

# EM-DAT Ingest

Loaded the full EM-DAT global natural disasters export and produced a cleaned parquet for
use in the liability pipeline.

## Key Numbers

| Metric | Value |
|--------|-------|
| Raw records | 27,642 entries (47 columns) |
| Natural disasters saved | 17,849 records |
| Raw file size | 22.9 MB |
| Processed parquet size | 4.15 MB |
| AU natural disasters | 231 |
| Wildfire records (global) | 516 |

## Black Summer Validation

EM-DAT contains **2 wildfire records** for AUS 2019:

| DisNo. | Name | total_damage_usd | total_damage_usd_2020 |
|--------|------|------------------|-----------------------|
| REDACTED-DISNO | (unnamed) | NaN | NaN |
| REDACTED-DISNO | Currowan | (redacted) | (redacted) |

**Key finding**: EM-DAT fragments Black Summer into individual named fire events rather than
recording the season as a whole. The per-event record (value redacted, EM-DAT DUA) is far below the Parliamentary
Budget Office whole-of-season direct economic estimate of AUD 10B (USD 6.9B). For Black Summer,
hardcoded PBO/ICA scenarios remain primary.

**Generalization implication**: EM-DAT is reliable for discrete events (single flood, cyclone,
earthquake) that map 1:1 to a `DisNo.` — `get_event_damages()` works as intended. For complex
multi-month fire seasons, EM-DAT understates totals. When applying the pipeline to a new event,
check `search_events()` record count first: if >1 match, decide whether to sum sub-events or
use an external aggregate source.

## Methodology

- Raw file: `data/raw/emdat/emdat_global_natural.csv` (22.9 MB, gitignored)
- Filtered to `Disaster Group = Natural`
- Damage columns converted from `'000 US$` to full USD (×1000)
- CPI-adjusted to 2020 USD using hardcoded BLS CPI-U table (1990–2023); events before 1990 use
  nominal values
- Column names normalised across EM-DAT export versions via fuzzy match

## Outputs

- `data/processed/emdat_disasters.parquet` — 17,849 natural disaster records (gitignored)
- `src/data/emdat.py` — `load_emdat()`, `search_events()`, `get_event_damages()` helpers
- EM-DAT lookup cell in `notebooks/03-liability/01_black_summer_liability.ipynb` (graceful skip
  if parquet absent)

## Data Attribution

EM-DAT: The Emergency Events Database — Université catholique de Louvain (UCL) — CRED,
D. Guha-Sapir — www.emdat.be, Brussels, Belgium. (Data Use Agreement — no redistribution)

## Related

- [[datasets/emdat]] — dataset documentation, T&C compliance, column reference
- [[disasters/black-summer-2019-20]] — event validated against EM-DAT
- [[2026-05-18-black-summer-liability]] — liability pipeline that uses damage estimates
