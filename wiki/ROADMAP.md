---
type: roadmap
tags: [platform, generalisation, web-app, agent, architecture]
related: [CONTEXT, methods/attribution-chain, findings/2026-06-24-literature-cross-check]
status: active
confidence: medium
last_updated: 2026-07-02
---

# Platform Roadmap — Generalisation, Explorer App, Agentic Ingestion

Decision record and phased plan for turning the two-event research pipeline into a platform:
(1) a public web app for exploring liabilities per location and over time, and (2) an agentic
capability for adding new disasters. Written 2026-07-02, immediately after the full pipeline
verification (16/16 validation benchmarks, bit-reproducible rebuild).

**Decisions taken (2026-07-02):**

| Decision | Choice |
|----------|--------|
| App architecture | **Static site + prebuilt JSON** exported from `data/processed` — no backend |
| Agent autonomy | **Draft + human review** — agent prepares everything, publishes nothing; PR review is the gate |
| Audience | **Public/advocacy + researchers/journalists** — headline layer with drill-down to uncertainty and provenance |
| Sequencing | Phase 1 (event-spec core) → Phase 2 (app MVP) → Phase 3 (agent) |

---

## 1. Generalisability Assessment (state of the pipeline, 2026-07-02)

**Verdict: the science core generalises; the event layer does not yet.** Both product directions
depend on closing that gap first, so it is Phase 1.

### Event-agnostic today (proven on two events)

| Asset | What it provides |
|-------|------------------|
| `data/processed/entity_warming_contribution.parquet` | Per-entity global warming shares — event-independent, computed once (FaIR, 841-config AR6 ensemble) |
| `src/attribution/shift_fit.py` (`shift_fit_gev`) | Nonstationary GEV shift-fit: additive (temperature) and multiplicative (precipitation) modes, seeded bootstrap |
| `src/attribution/liability.py` (`build_liability_table`, `far`) | Global-share apportionment + PR-bootstrap uncertainty, any damage-scenario set |
| `src/attribution/seasonal.py`, `gmst.py` | Area-weighted series, season block maxima, N-day precip maxima; FaIR GMST covariate helpers |
| `src/attribution/validation.py` + `tests/validation_benchmarks.json` | Literature/internal/golden benchmark harness; exits non-zero on drift |
| `src/data/emdat.py` | EM-DAT search and damage lookup (17,849 records) |

### Still per-event and manual

- **Event definition is code, not data**: region bbox, season months, metric, GEV mode, β, and
  damage scenarios are hand-written cells in `scripts/build_notebooks.py` — duplicated per event.
- **ERA5 acquisition is manual**: CDS requests, quota-aware decade batching (4×/day sampling) —
  process knowledge lives in CLAUDE.md prose, not code.
- **β / regional amplification requires scientific judgment**: choosing the primary vs sensitivity
  estimate is not mechanical. The orphan QLD α=0.289 (`ERA5_observed` row carried in
  `qld_amplification_factor.csv` with no reproducible producer) is the cautionary example — see
  [[findings/2026-06-17-lei-dropna-fix]].
- **Damage scenarios require research**: each figure needs a defensible source — the QLD central was
  an unsourced AUD 10B placeholder until verified against Deloitte (AUD 7.7B) on 2026-07-05
  ([[findings/2026-07-05-qld-damage-verification]]); the event-spec schema must therefore carry a
  citation per damage figure.
- **Validation benchmarks are hand-pinned** per event in `tests/validation_benchmarks.json`.
- **Constants are Australia-shaped**: `AUD_TO_USD` in `src/attribution/constants.py`; no general
  FX/CPI handling.

### Hazard and scope limits

- **Supported**: heat extremes (additive shift, block-max temperature) and precipitation extremes
  (multiplicative shift, Clausius-Clapeyron β = ln(1+CC)·α).
- **Not supported without new methodology**: wind/tropical-cyclone intensity, drought duration,
  compound events, coastal/surge flooding, slow-onset losses.
- FaIR GMST ends 2021; `extrapolate_to` covers nearby years but a refresh run will eventually be
  needed for post-2021 events.
- CO₂e-consistent global denominator (non-CO₂ forcers) is still a tracked refinement
  ([[methods/emissions-to-forcing]]).

---

## 2. Phase 1 — Event-Spec Core (shared foundation)

Make "an event" a declarative artifact instead of hand-written notebook cells.

- **`events/<slug>.yaml`** — one file per disaster:
  - metadata: name, dates, EM-DAT id, wiki disaster page slug
  - hazard template: `heat_blockmax` | `precip_ndaymax` (constrains metric + GEV mode)
  - region bbox, season months, event year, ERA5 source file
  - β specification: primary (value + source + justification) and sensitivities
  - damage scenarios: amount, currency, year, FX rate, source citation, **and geographic scope**
    each — the scope field is load-bearing, not cosmetic: the QLD event mixes a QLD+NSW insured
    floor (AUD 5.81B) with a QLD-only total (AUD 7.7B), and only an explicit scope makes that
    mismatch visible rather than buried in prose (see [[findings/2026-07-05-qld-damage-verification]]).
    `run_event` should warn when scenarios of differing scope are ordered as conservative→central,
    and never silently treat a wider-scope figure as directly comparable to a narrower one.
- **`src/attribution/event.py`** — `load_event(slug)` + `run_event(spec)` producing the existing
  artifact set with current naming conventions (`<slug>_pr_era5.csv`, `<slug>_pr_shiftfit_bootstrap.parquet`,
  `<slug>_liability.parquet`, `<slug>_scenario_totals.csv`).
- **Acceptance criterion**: Black Summer and QLD floods, expressed as YAML, reproduce today's
  outputs **bit-for-bit** (bootstrap is seeded), gated by the existing validation harness.
  Per-event golden benchmarks derived from the spec rather than hand-edited JSON.
- **`src/data/era5.py`** — CDS fetcher encoding the quota-aware decade-batching procedure
  (currently CLAUDE.md prose) so data acquisition is reproducible and agent-callable.
- **Proof of generality**: add a **third event via YAML only** (already a project next step).
  A non-Australian event would also force the FX/CPI generalisation.
- Fold in the standing hygiene item: a reproducible producer for the QLD wet-season α=0.289.

## 3. Phase 2 — Static Explorer App (map + time)

- **`scripts/export_web_catalog.py`** — `data/processed` → JSON:
  - `catalog.json`: events with footprint geometry (bbox → GeoJSON), dates, PR/FAR with 5–95%
    ranges, damage scenarios, scenario totals
  - `events/<slug>.json`: full per-entity liability table
  - `entities.json`: warming shares plus cumulative emissions/warming timeseries (from
    `cm_entity_year.parquet` + `fair_global_temperature.parquet`) — this is the "over time" axis
- **Static site** (Next.js or Astro; no backend, deployable to brigid.earth):
  - **Map view**: event footprints, colored by attributed liability
  - **Timeline view**: events by date; entity cumulative-warming trajectories
  - **Event page**: headline liability → drill-down to entity table with uncertainty ranges and a
    damage-scenario toggle
  - **Entity page**: warming share, liability across events, emissions history
  - **Methodology page**: linking the published wiki (findings/methods/references)
- **Dual-audience layering**: headline numbers first (public/advocacy); one click down reveals
  5–95% ranges, PR-method sensitivities, and provenance links to wiki findings and references
  (researchers/journalists). Consider publishing the wiki alongside the app.
- **Guardrails**:
  - Preserve the project convention: physical attribution ("contribution to risk") strictly
    separate from legal liability framing, on every page.
  - **EM-DAT figures must never be surfaced in the public app** (verified 2026-07-05,
    [[datasets/emdat]]): the Terms of Use prohibit transmitting any portion to unauthorised users
    (the public) and creating derivative databases. The exporter must read damages from the
    independently-sourced event specs, not `emdat_disasters.parquet`.
  - QLD central damages (AUD 10B) must be verified (Deloitte / QLD Treasury / NEMA) before the
    number is public-facing.

## 4. Phase 3 — Agentic Disaster Ingestion (draft + human review)

- **Flow**: input (EM-DAT id or event description) →
  1. research: EM-DAT record, WWA/literature search, damage sources
  2. draft `events/<slug>.yaml` + `wiki/references/` pages for new citations
  3. fetch ERA5 via `src/data/era5.py`
  4. run `run_event` + validation harness
  5. draft the dated `wiki/findings/` page and proposed benchmark entries
  6. open a **PR with a structured review checklist**: region/season definition, β choice and
     justification, damage scenario sources, validation report
- **Human review is the gate**: the agent never merges. Merging triggers catalog re-export and
  site rebuild.
- **Implementation**: start as a **Claude Code skill in this repo** (lowest lift; reuses the
  existing tools, harness, and wiki conventions). Graduate to a Claude Agent SDK service only when
  the platform needs unattended operation.
- **Constraint**: the agent is restricted to the supported hazard templates (heat, precip). New
  hazard types require human methodology work first — the templates encode that boundary.

## 5. Open Questions

- ~~QLD AUD 10B central damage verification~~ **RESOLVED 2026-07-05**: the AUD 10B/20B placeholders
  had no source. Authoritative anchor is **Deloitte Access Economics AUD 7.7B total cost (QLD only)**,
  commissioned by the QLD Government, June 2022 — of which ~AUD 3.2B tangible/direct and AUD 4.5B
  intangible/social. ICA insured (final) AUD 5.81B is a QLD+NSW-scope lower bound. **Resolved**: the
  pipeline now uses conservative AUD 5.81B (insured) + central AUD 7.7B (Deloitte total), retiring
  the AUD 20B comprehensive; QLD headline liability USD 0.38B → **USD 0.29B**. See
  [[findings/2026-07-05-qld-damage-verification]].
- ~~EM-DAT Data Use Agreement — what derived figures may appear publicly~~ **RESOLVED 2026-07-05**:
  EM-DAT terms prohibit transmitting any portion to unauthorised users (the public), creating
  derivative databases, and commercial use. **EM-DAT figures must not appear in the public app.**
  No pipeline change — EM-DAT is already an internal cross-check only; the Phase 2 exporter must pull
  damages from the independently-sourced event specs, not `emdat_disasters.parquet`. See
  [[datasets/emdat]].
- Non-Australian events: ERA5 coverage is global, but FX/CPI conversion must generalise beyond
  `AUD_TO_USD`.
- CO₂e-consistent denominator (non-CO₂ forcers) — changes the collective share modestly.
- GEV distribution-form uncertainty (single parametric fit per pool today).
- Hosting/deployment target for brigid.earth; whether the wiki is published with the app.
