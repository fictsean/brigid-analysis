---
type: disaster
name: black-summer-2019-20
tags: [bushfire, australia, heat, fire-weather, 2019, 2020]
related: [wwa-studies, far-probability-ratio, findings/2026-05-18-black-summer-liability, findings/2026-05-23-australia-regional-amplification, findings/2026-05-24-black-summer-pr-era5, findings/2026-05-24-observed-amplification, era5-reanalysis, cmip6]
status: active
confidence: medium
last_updated: 2026-07-02
---

# Black Summer 2019–20 (Australian Bushfires)

## Event Summary

- **Dates**: October 2019 – March 2020 (peak: December 2019 – January 2020)
- **Region**: Southeastern Australia (NSW, Victoria, SA, ACT)
- **Area burned**: ~24 million hectares
- **Buildings destroyed**: 3,000+
- **Direct deaths**: 33
- **Smoke-related deaths**: ~417 (estimated)

## Attribution

### WWA (Published)
**Source**: van Oldenborgh et al. (2021), *Nat. Hazards Earth Syst. Sci.* https://doi.org/10.5194/nhess-21-941-2021

| Metric | PR | FAR |
|--------|-----|-----|
| Fire Weather Index (FWI) | ≥4 | ≥0.75 |
| Monthly Severity Rating (MSR) | ≥9 | ≥0.89 |

### Nonstationary GEV Shift-Fit (Primary)
**Source**: `notebooks/02-attribution/04_black_summer_pr_era5.ipynb`; `src/attribution/shift_fit.py`

The observed ERA5 pool is rescaled to the pre-industrial climate via a smoothed FaIR GMST covariate
(shift coefficient β = α_ERA5 = 0.726), with a GEV fitted to the fire-season block maxima. See
[[2026-06-13-methodology-revision]] for why this replaced the earlier detrended-Gaussian approach.

| Method | PR | FAR | Notes |
|--------|-----|-----|-------|
| **GEV shift-fit, β=0.726 (ERA5)** | **4.0 [2.4–15.4]** | **0.752** | **Primary estimate** |
| GEV shift-fit, β=0.935 (CMIP6 tas) | 6.3 [3.3–35] | 0.842 | Sensitivity |
| WWA ERA5 FWI7x-SM lower bound | >4 | >0.75 | Validation reference |
| WWA model-FWI (conservative) | ≥1.3 (≥30%) | ≥0.23 | Context (models underestimate) |
| WWA MSR central | >9 | >0.89 | Validation reference |

The primary PR sits at the WWA **ERA5 FWI7x-SM** lower bound (">4") — the observational metric, not
the model-based FWI ("≥30%"). See [[findings/2026-05-24-black-summer-pr-era5]].

### CMIP6 Independent Verification (Null Result)
Computed in `notebooks/02-attribution/03_black_summer_pr_cmip6.ipynb` using `tasmax` Oct–Mar seasonal maxima from 4 CMIP6 models (19 member-runs). **Null result**: CMIP6 PR = 0.6, opposite of physical expectation. The available models do not reproduce the Australian warming signal — consistent with the amplification underestimation found in [[findings/2026-05-23-australia-regional-amplification]]. WWA PR values are authoritative.

See [[findings/2026-05-24-black-summer-pr-cmip6]] for full analysis.

## Damages

| Estimate | AUD (B) | Source |
|----------|---------|--------|
| Insured losses | 2.32 | Insurance Council of Australia |
| Direct economic | ~10 | Parliamentary Budget Office |
| Total social cost | ~103 | Filkov et al. (2020); Deloitte |

## Liability Analysis

See [[findings/2026-05-18-black-summer-liability]] for full entity-level breakdown.

Central scenario (AUD 10B direct damages, FAR=0.752): total Carbon Majors attributed liability =
**USD 2.78B** (primary, PR=4.0). Top entity Former Soviet Union USD 289M, then China Coal USD 225M;
Saudi Aramco USD 139M [109–173]. Carbon Majors cover ~54% of total anthropogenic CO₂ (FFI + AFOLU),
so this is that fraction of climate-attributed damages — matching the peer-reviewed benchmark
(Stuart-Smith et al. 2025, *Nature*). See [[findings/2026-06-24-literature-cross-check]] for the
denominator fix that revised these from the earlier 3.92B.

The regional amplification (α=0.726, ERA5 fire-season) enters as the shift coefficient β in the PR,
not as a liability multiplier — see [[regional-amplification]] and [[2026-06-13-methodology-revision]].

## Litigation Context

Black Summer has been cited in several Australian climate litigation cases and regulatory proceedings. The fires contributed to political pressure that led to Australia's updated 2030 and 2050 climate targets under the Climate Change Act 2022.
