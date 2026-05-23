---
type: disaster
name: black-summer-2019-20
tags: [bushfire, australia, heat, fire-weather, 2019, 2020]
related: [wwa-studies, far-probability-ratio, 2026-05-18-black-summer-liability, 2026-05-23-australia-regional-amplification, era5-reanalysis, cmip6]
status: active
confidence: medium
last_updated: 2026-05-23
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

### CMIP6 Independent Verification
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

Central scenario (AUD 10B direct damages, PR=9): total Carbon Majors attributed liability = **USD 6.1B**, with Saudi Aramco (USD 521M) and ExxonMobil (USD 439M) as top entities.

Regional warming shares for SE Australia incorporate a CMIP6-derived amplification factor of 0.935 (ensemble median). Using the BoM-observed amplification (~1.35) would increase estimates by ~45%. See [[findings/2026-05-23-australia-regional-amplification]].

## Litigation Context

Black Summer has been cited in several Australian climate litigation cases and regulatory proceedings. The fires contributed to political pressure that led to Australia's updated 2030 and 2050 climate targets under the Climate Change Act 2022.
