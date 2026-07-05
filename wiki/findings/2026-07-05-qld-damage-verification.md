---
type: finding
name: 2026-07-05-qld-damage-verification
description: QLD floods damage verified — Deloitte AUD 7.7B total cost replaces unsourced AUD 10B placeholder (central USD 0.38B→0.29B); EM-DAT Terms of Use bar surfacing EM-DAT figures in the public app
tags: [damages, floods, queensland, emdat, licence, verification, liability]
related: [disasters/qld-floods-2022, datasets/emdat, findings/2026-05-26-qld-floods-liability, ROADMAP, references/comm-earth-env-2025-feb2022-floods]
status: settled
confidence: high
last_updated: 2026-07-05
---

# 2022 QLD Floods — Damage & EM-DAT Licence Verification

Two roadmap blockers ([[ROADMAP]]) resolved before building the platform: (1) the QLD central
damage figure, and (2) whether EM-DAT data may appear in a public app.

## 1. QLD central damages — AUD 10B was unsourced; the anchor is Deloitte AUD 7.7B

The AUD 10B "central / direct economic" and AUD 20B "comprehensive" scenarios were **unsourced
placeholders** — no source supported them. Verification (web, 2026-07-05) found a single
authoritative total-cost study of exactly our event:

**Deloitte Access Economics, *The social, financial and economic costs of the 2022 South East
Queensland Rainfall and Flooding Event*, commissioned by the Queensland Government / Queensland
Reconstruction Authority, June 2022.** Covers 23 LGAs (Gladstone → Gold Coast → Balonne), **QLD
only** — matching our SE QLD event footprint.

| Component | AUD | Notes |
|-----------|-----|-------|
| **Total cost** | **7.7B** | economic + social |
| — intangible / social | 4.5B | >500,000 people affected |
| — homes & commercial buildings | 2.0B | ~18,000 properties |
| — small business | 0.32B | 4,500+ businesses |
| — agriculture | 0.25B | 2,250+ primary producers |
| — public infrastructure & other | ~0.65B | remainder |
| — of which tangible/direct (sum) | ~3.2B | |

Cross-reference: **ICA final insured losses AUD 5.81B** (240,000+ claims, published April 2023) —
but that is the wider **QLD + NSW** event, so a scope-mismatched lower bound (insured < total; QLD
is the bulk, so ordering still holds).

### Decision (user, 2026-07-05): Deloitte AUD 7.7B total as central

Scenario set is now **two** figures, both sourced:

| Scenario | AUD | Source | Scope |
|----------|-----|--------|-------|
| conservative | 5.81B | ICA insured (final) | QLD + NSW |
| central | 7.7B | Deloitte total cost | QLD |

The unsourced AUD 20B comprehensive was retired. Alternative mappings considered and rejected:
tangible-only AUD 3.2B as central would have fallen *below* the insured floor (scope artefact).

### Headline impact

| Quantity | Before (AUD 10B) | After (AUD 7.7B) |
|----------|------------------|------------------|
| QLD central total CM liability | USD 0.38B | **USD 0.29B** |
| Saudi Aramco (central) | USD 19.0M | **USD 14.6M** [7.5–33] |
| Former Soviet Union (central) | USD 39M | **USD 30M** |

Only the damage input changed; PR/FAR (1.11 / 0.101), warming shares, and apportionment are
untouched. Golden benchmark `qld_central_usd_b` re-frozen to [0.284, 0.298]; full harness 16/16 PASS.

## 2. EM-DAT — figures cannot appear in the public app

The [EM-DAT Terms of Use](https://doc.emdat.be/docs/legal/terms-of-use/) (verified 2026-07-05) are a
restricted conditional licence, **not** open/CC-BY. Users shall not "Share, use or transmit any
portion of EM-DAT via the Internet to unauthorized users", nor "Create substitute or derivative
databases of EM-DAT", nor make commercial use without a paid agreement. The general public are not
authorised users.

**Conclusion**: EM-DAT-derived figures **must not be surfaced in the public explorer app**. No
pipeline change is required — the pipeline already uses EM-DAT only as an internal validation
cross-check, with independently-sourced ICA/Deloitte/government figures as the primary
`total_damages`. **Guardrail for Phase 2**: `scripts/export_web_catalog.py` must read damages from
the event specs, never from `emdat_disasters.parquet`. See [[datasets/emdat]].

## Sources

- Deloitte / QRA report (June 2022): https://www.qra.qld.gov.au/2021-22-Southern-Queensland-Floods
- QLD Government statement (AUD 7.7B): https://statements.qld.gov.au/statements/95831
- ICA final insured loss (AUD 5.81B): https://insurancecouncil.com.au/resource/2022-flood-now-third-costliest-natural-disaster-ever/
- EM-DAT Terms of Use: https://doc.emdat.be/docs/legal/terms-of-use/
