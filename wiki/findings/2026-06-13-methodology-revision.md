---
type: finding
name: 2026-06-13-methodology-revision
description: Methodology review fixes — global-share apportionment, GEV shift-fit PR, real uncertainty propagation, removed invalid PR×ratio correction; Black Summer central 5.08B→2.31B
tags: [methodology, review, liability, attribution, gev, apportionment, uncertainty]
related: [attribution-chain, far-probability-ratio, regional-amplification, emissions-to-forcing, 2026-05-18-black-summer-liability, 2026-05-24-black-summer-pr-era5, 2026-05-26-qld-floods-liability, 2026-05-26-qld-floods-pr-era5, 2026-05-24-observed-amplification]
status: settled
confidence: high
last_updated: 2026-06-13
---

# Methodology Revision — 2026-06-13

A full methodology review surfaced several errors affecting every published liability number. All
were fixed in one pass; the attribution chain was also refactored into `src/attribution/` with the
notebooks reduced to thin callers. This page is the canonical record of what changed and why.

> **Superseded headline numbers (2026-06-17).** The "After" column below reflects the state
> *immediately after the 2026-06-13 revision*, when `cm_entity_year.parquet` still had the LEI-dropna
> data-loss bug. That bug was fixed on 2026-06-17 ([[2026-06-17-lei-dropna-fix]]), which raised
> collective coverage 44.6% → 75.5% and moved Black Summer central to **USD 3.92B** and QLD central to
> **USD 0.53B**. The *methodology* described on this page is unchanged and still current — only the
> headline magnitudes were revised again by the data fix. Saudi Aramco and other LEI-holding
> incumbents are unchanged.

## Headline number changes

| Quantity | Before | After (2026-06-13; see note for current) |
|----------|--------|-------|
| Black Summer central CM liability | USD 5.08B | **USD 2.31B** |
| Black Summer Saudi Aramco (central) | USD 261–431M (scenario-dependent) | **USD 196M [154–244]** |
| Black Summer primary PR / FAR | 3.8 / 0.736 (detrended Gaussian) | **4.0 / 0.752** (GEV shift-fit) |
| QLD floods central CM liability | USD 0.73B | **USD 0.31B** |
| QLD floods Saudi Aramco (central) | USD 62M | **USD 27M [13–61]** |

## Fixes

### 1. Apportionment — global share, not Carbon-Majors-normalised (critical)
The liability notebooks divided each entity's warming by the **Carbon Majors total** (shares summed
to 1.0), charging the named group 100% of climate-attributed damages despite covering only ~45% of
global warming — inflating every entity ~2.2×. Now `liability = global_warming_share × FAR ×
damages`, using `global_share` directly (`build_liability_table` in `src/attribution/liability.py`).

### 2. Real uncertainty propagation (critical)
The old p05/p95 "FaIR uncertainty" columns were identical to machine precision: warming = share ×
ΔT, so ΔT cancels in any share ratio. The FaIR ensemble contributes **zero** liability spread.
Liability uncertainty now comes from the **PR bootstrap** (5–95% of FAR), propagated per scenario.

### 3. Invalid PR × amplification-ratio correction removed (critical)
Notebook 05 computed `PR_obs = PR × (α_obs/α_cmip6)`. PR is a nonlinear function of the
distributional shift and does not scale linearly with an amplification ratio. The `liability_obs_*`
columns and the USD 1.96B figure derived from it are removed. The amplification factor enters
**correctly** as the shift coefficient β inside the shift-fit.

### 4. Nonstationary GEV shift-fit replaces detrended Gaussian (significant)
The old "detrended ERA5" P0 removed only warming since the 1961–1990 baseline (not since
pre-industrial) and fitted Gaussian/log-normal tails near the record maximum. The new method
(`src/attribution/shift_fit.py`) rescales the observed pool to pre-industrial via a smoothed FaIR
GMST covariate (counterfactual covariate = 0) and fits a **GEV** to the block maxima — additive for
temperature, multiplicative (Clausius-Clapeyron) for precipitation. Black Summer PR=4.0 now matches
the WWA FWI lower bound exactly.

### 5. α metric mislabel corrected (documentation)
The CMIP6 SE-AU amplification (0.935) was documented as "fire-season tasmax" but notebook 02
computes **annual-mean tas**. All wiki/CLAUDE references corrected; the ERA5 fire-season value
(0.726) is the primary β.

### 6. QLD CMIP6 hist-nat "null result" reframed (significant)
The PR=0.44 compared an ERA5-unit precipitation threshold against a CMIP6 distribution with no
bias/quantile correction — a units confound, not a clean model signal. Dropped from the primary
path and reframed.

### 7. Smaller fixes
- Dead `thr = np.random.choice(h)` removed from the QLD bootstrap.
- ERA5 mx2t is an hourly max at 06 UTC, not a 24-hour max — comments corrected.
- Scenario axes de-conflated: one primary FAR across damage scenarios, plus a PR × damages grid.
- Single `AUD_TO_USD` source of truth (`src/attribution/constants.py`), keyed by year.
- Circular notebook dependency removed: PR notebooks (04, 07) write bootstrap parquets that the
  liability notebooks (01, 02) read — a clean one-way DAG. Incomplete edge seasons dropped from
  block-maxima pools.
- Unit caveat noted: entity CO₂e numerator vs global CO₂-FFI denominator (see [[emissions-to-forcing]]).

## What did not change
Carbon Majors ingest, FaIR warming attribution, entity warming shares, and the CMIP6/ERA5
amplification *values* are unchanged. The PR being close to the old value (3.8 → 4.0) is
reassuring; the large liability drop is driven almost entirely by the apportionment fix (#1).
