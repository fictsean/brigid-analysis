---
type: finding
name: 2026-05-15-carbon-majors-ingest
tags: [carbon-majors, emissions, data-ingestion]
related: [carbon-majors-database, emissions-to-forcing]
status: active
confidence: high
last_updated: 2026-05-15
notebook: notebooks/01-exploration/02_carbon_majors_ingest.ipynb
---

# Carbon Majors Ingest — Initial Findings

First load of the Carbon Majors high-granularity dataset (InfluenceMap 2026 release, 1854–2024).

## Key Numbers

| Metric | Value |
|--------|-------|
| Total cumulative emissions (1854–2024) | **1,435.6 GtCO₂e** |
| Entities in dataset | 178 |
| Top single emitter | Former Soviet Union (1900–1991) — **9.4%** of all-time total |
| Entities needed for 50% of emissions | **13** |
| Scope 3 share (product combustion) | **88.1%** |
| Scope 1 share (operational) | **11.9%** |
| Post-1988 share of all-time emissions | **69.0%** |

## Validation

Cross-check against published launch report figure (1,421 GtCO₂e through 2022): our load gives 1,406 Gt through 2022 — within ~1%, consistent with minor methodology updates in the 2026 release. Scope totals and entity counts match documentation.

## Notable Observations

- **Concentration is extreme**: 13 entities account for half of all historical emissions; the top 3 alone (Former Soviet Union, Saudi Aramco, Chevron) exceed 20%.
- **Scope 3 dominates**: 88% of attributed emissions come from end-use combustion of sold products, not direct operations. This is the legally contested scope — many liability frameworks focus on scope 1 only.
- **Post-1988 recency**: 69% of all attributed emissions occurred after James Hansen's 1988 Congressional testimony establishing public scientific awareness of climate change. This is legally significant for "knew or should have known" arguments.
- **Nation-state category**: Former Soviet Union (1900–1991) is the top entity but is historical — current Russia and successor states are tracked separately from 1992 onward.

## Outputs

- `data/processed/cm_entity_year.parquet` — 8,618 rows; entity × year with full emissions breakdown
- `data/processed/cm_cumulative_summary.parquet` — 178 rows; cumulative totals and global share per entity across three time windows
- `data/processed/cm_global_annual.parquet` — annual global totals by parent type

## Next Steps

- Cross-reference entity list against EM-DAT disaster records to identify which entities are defendants in existing climate litigation
- ✅ Fed into FaIR v2.2 — see [[2026-05-15-emissions-to-warming]]
