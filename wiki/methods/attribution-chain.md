---
type: method
name: attribution-chain
tags: [overview, attribution, liability, end-to-end]
related: [emissions-to-forcing, far-probability-ratio, regional-amplification, carbon-majors-database, era5-reanalysis, cmip6, ekwurzel-2017, 2026-06-13-methodology-revision]
status: active
confidence: high
last_updated: 2026-06-13
---

# Attribution Chain — End-to-End Overview

This page describes the full methodology for calculating an entity's proportional liability for a
specific climate disaster. It is the entry point before reading the individual method pages or
notebooks. Terms in **bold** are defined on first use.

> **Revised 2026-06-13** ([[2026-06-13-methodology-revision]]). The PR step now uses a nonstationary
> GEV shift-fit (referenced to pre-industrial), and apportionment uses each entity's **global**
> warming share. The code lives in `src/attribution/`; notebooks are thin callers.
>
> **Data fix 2026-06-17** ([[2026-06-17-lei-dropna-fix]]). The entity-year aggregation was silently
> dropping ~562 GtCO₂e of null-LEI emitters (Former Soviet Union, China Coal, Chevron, NIOC…).
>
> **Denominator fix 2026-06-24** ([[2026-06-24-literature-cross-check]]). The warming-share denominator moved from fossil-CO₂-only to **total anthropogenic CO₂ (FFI + AFOLU)**, correcting an over-attribution: collective coverage **53.6%** (was 75.5%), matching Stuart-Smith et al. 2025 (~54%). Black Summer central liability is now **USD 2.78B**. A validation harness (`scripts/validate_pipeline.py`) now pins these against literature/internal benchmarks.

## The Chain

```
Named Emitter
    │
    │ historical emissions record (Carbon Majors database)
    ▼
Cumulative Emissions
    │
    │ simple climate model (FaIR v2.2, AR6-calibrated)
    ▼
Global Warming Contribution  (°C attributable to this entity)
    │
    │ regional amplification factor
    ▼
Regional Warming Contribution
    │
    │ probabilistic event attribution (ERA5 + CMIP6 hist-nat)
    ▼
Fraction of Event Risk Attributable to Climate Change (FAR)
    │
    │ apply to event damage estimate
    ▼
Climate-Attributed Damages
    │
    │ apportion by entity warming share
    ▼
Entity Liability (USD)
```

---

## Step 1 — Named Emitter → Cumulative Emissions

The starting point is a historical record of which companies and governments extracted and sold
fossil fuels. We use the **Carbon Majors database** (Heede 2014, updated by the Climate
Accountability Institute), which tracks ~100 major fossil fuel producers from 1854 to the present.

Emissions in this database include three "scopes":
- **Scope 1**: emissions from the extraction and production process itself (e.g., gas flaring)
- **Scope 2**: emissions from the company's own energy use
- **Scope 3**: emissions from burning the fossil fuels the company extracted and sold to customers

Scope 3 accounts for ~88% of the total. This is the contested category: is a company responsible
for the emissions that occur when a consumer burns the fuel it produced? The database includes all
three; we report liability estimates with and without scope 3 as a sensitivity.

**Key numbers**: ~1,435 GtCO₂e (gigatonnes of CO₂ equivalent) total across all producers;
13 entities = 50% of cumulative emissions; 69% of emissions occurred after 1988.

**Notebook**: `01-exploration/02_carbon_majors_ingest.ipynb`  
**Output**: `data/processed/cm_entity_year.parquet`, `cm_cumulative_summary.parquet`  
**Wiki**: [[datasets/carbon-majors-database]]

---

## Step 2 — Cumulative Emissions → Global Warming Contribution

Each entity's share of cumulative global fossil emissions translates into a share of observed
global warming. This relies on a well-established physical relationship called **TCRE** (Transient
Climate Response to Cumulative CO₂ Emissions): global mean temperature rise scales approximately
linearly with cumulative CO₂ emissions. Because the relationship is linear, proportionality holds:

```
entity_warming_share = entity_cumulative_CO2e / global_cumulative_fossil_CO2
entity_warming_°C    = entity_warming_share × ΔT_global
```

We run this through **FaIR v2.2**, a simple climate model calibrated to the IPCC Sixth Assessment
Report (AR6). FaIR takes all-entity emissions as input and outputs global mean surface temperature
over time, letting us compute each entity's marginal contribution. We use an ensemble of 841
parameter configurations (a "posterior ensemble") to produce a probability range (5th–95th
percentile) rather than a single number.

**Validation**: FaIR's median gives 1.04°C of warming for 2011–2020 against the IPCC AR6 best
estimate of 1.07°C.

**Key result**: Carbon Majors collectively responsible for ~54% of observed 1.18°C warming (0.63°C),
matching Stuart-Smith et al. 2025 (~54%) and Ekwurzel 2017 (~42–50%).
Former Soviet Union: 65.9 m°C; China Coal: 51.1 m°C; Saudi Aramco: 31.7 m°C (where m°C = millidegrees Celsius).

**Notebook**: `02-attribution/01_emissions_to_warming.ipynb`  
**Output**: `data/processed/entity_warming_contribution.parquet`, `fair_global_temperature.parquet`  
**Wiki**: [[methods/emissions-to-forcing]], [[findings/2026-05-15-emissions-to-warming]]

---

## Step 3 — Global → Regional Warming

Entity warming shares are computed globally. Climate events are regional. The global average
warming does not apply uniformly — some regions warm faster or slower than the world average.

The **regional amplification factor** (α, "alpha") captures this:

```
α = regional_warming_trend / global_warming_trend
```

α > 1 means the region warmed faster than the global average; α < 1 means it warmed more slowly.

α enters the chain as the **shift coefficient β** in the Step-4 PR computation: it sets how far the
observed record is rescaled between the factual and pre-industrial climates. A larger β produces a
larger shift and a higher PR — a *nonlinear* dependence. α does **not** multiply into the final
liability, which uses each entity's global warming share directly.

**Current estimates for SE Australia**:

| Source | α | What was measured |
|--------|---|-------------------|
| ERA5 observed (**primary β**) | 0.726 | Observed *fire-season* daily-max temperature vs FaIR GMST, 1961–2020 |
| CMIP6 models (ACCESS-CM2 + ACCESS-ESM1-5) | 0.935 | Model *annual-mean* tas vs model global mean, 1901–2014 |

The two are **different metrics** (fire-season mx2t vs annual-mean tas) and are not directly
comparable; the ERA5 fire-season value is used as primary. BoM reports SE Australian annual-mean warming ~1.3–1.5× global since 1910 — a third, different metric.

**Notebooks**: `02-attribution/02_australia_regional_amplification.ipynb`,
`02-attribution/05_observed_amplification.ipynb`  
**Wiki**: [[methods/regional-amplification]], [[findings/2026-05-23-australia-regional-amplification]],
[[findings/2026-05-24-observed-amplification]]

---

## Step 4 — Regional Warming → Event Probability Change (PR / FAR)

This step answers: *how much more likely was this event because of climate change?*

**Probability Ratio (PR)**: the ratio of the probability of the event in today's climate (the
"factual" world with human-caused emissions) to the probability in a hypothetical world where
humans had not emitted greenhouse gases (the "counterfactual").

```
PR = P1 / P0
```

- P1 = probability of the event in the factual (warmed) climate
- P0 = probability of the event in the counterfactual (natural-forcing-only) climate
- PR = 2 means the event is twice as likely today as it would have been without climate change

**Fraction of Attributable Risk (FAR)**: translates PR into a fraction of damages.

```
FAR = 1 - 1/PR
```

FAR = 0.44 (44.4%) means that 44.4% of the event's risk is attributable to climate change.

### Factual distribution (P1)

We use **ERA5** — the ECMWF Reanalysis v5 — which reconstructs the observed state of the
atmosphere from 1940 to present by combining weather station, satellite, and radiosonde data
through a numerical model. It gives a gridded, continuous, physically consistent record of
observed weather.

The specific variable is **mx2t** (maximum 2-metre temperature): the highest near-surface air
temperature recorded over a 24-hour window at each grid point. This is equivalent to the
climate model variable called **tasmax** (daily maximum near-surface air temperature). We compute the fire-season (October–March) anomaly for SE Australia.

### Counterfactual distribution (P0) — nonstationary GEV shift-fit

We build P0 from the **same observed ERA5 pool**, rescaled to a pre-industrial climate using a
smoothed FaIR GMST covariate (the WWA "shift-fit"). Each season is shifted by β·ΔG — additively
for temperature, multiplicatively (Clausius-Clapeyron) for precipitation — where the counterfactual
GMST is 0 vs 1850–1900, so the shift removes *all* anthropogenic warming. A **GEV** (the natural
distribution for seasonal block maxima) is fitted to the factual pool; P0 is read from the same fit
at the threshold mapped to the counterfactual climate. A 2,000× bootstrap (resampling seasons +
sampling FaIR event-year GMST uncertainty) gives the range.

This replaces the earlier Gaussian "ERA5 + CMIP6 hist-nat" / "detrended ERA5" approaches, which
mixed climatological baselines and evaluated Gaussian tails near the record maximum
([[2026-06-13-methodology-revision]]). No CMIP6 streaming is required for the PR.

**Why ERA5 for the pool**: the factual climate is the observed record, not a model's version of it
— the standard WWA choice.

**Primary result for Black Summer**: PR = 4.0 [2.4–15.4], FAR = 0.752 (shift coefficient β = 0.726).
This sits at the WWA **ERA5 FWI7x-SM** lower bound (">4"; the model-FWI result is "≥30%"). The data-driven fitted β (PR=18.7) is rejected as outlier-driven; CMIP6 hist-nat (notebook 03, PR=0.6) is a documented null result only.

**Notebooks**: `02-attribution/04_black_summer_pr_era5.ipynb` (primary),
`02-attribution/03_black_summer_pr_cmip6.ipynb` (null result)  
**Code**: `src/attribution/shift_fit.py`  
**Output**: `data/processed/black_summer_pr_era5.csv`, `black_summer_pr_shiftfit_bootstrap.parquet`  
**Wiki**: [[methods/far-probability-ratio]], [[findings/2026-05-24-black-summer-pr-era5]],
[[datasets/wwa-studies]]

---

## Step 5 — FAR × Damages → Climate-Attributed Damages

FAR is multiplied by a total damage estimate for the event. The interpretation: FAR% of the
damages would not have occurred in a world without anthropogenic climate change. The same primary
FAR is applied across damage scenarios — damages are a separate axis from PR, and a joint
PR × damages grid (see the liability notebooks) shows the combined sensitivity.

```
climate_attributed_damages = total_damages × FAR
```

**Damage scenarios** introduce the largest source of uncertainty — roughly a 120× range for
Black Summer alone:

| Scenario | Basis | AUD (B) | USD (B) |
|----------|-------|---------|---------|
| Conservative | Insured losses (Insurance Council of Australia) | 2.32 | 1.60 |
| Central | Direct economic losses (Parliamentary Budget Office; sectoral studies) | 10.0 | 6.90 |
| Comprehensive | Total social cost including health impacts (Filkov et al. 2020; Deloitte) | 103.0 | 71.1 |

For systematic multi-event analysis, we will use **EM-DAT** (Emergency Events Database), the
standard international disaster loss database maintained by the Centre for Research on the
Epidemiology of Disasters. EM-DAT registration is pending.

**Wiki**: [[disasters/black-summer-2019-20]]

---

## Step 6 — Entity Warming Share × FAR × Damages → Liability

The final step combines the entity's **global** warming share (Step 2), the FAR (Step 4), and the
total damage estimate (Step 5).

```
entity_liability_USD = entity_global_warming_share × FAR × total_damages_USD
```

The proportionality assumption: if entity X caused W% of *global* warming, they caused W% of the
climate-attributed fraction of damages. The named Carbon Majors collectively cover ~54% of total
anthropogenic CO₂ (FFI + AFOLU), so they absorb ~54% of the climate-attributed damages — the share is **not** normalised
within the group. This is a physical-science proportionality claim, not a legal ruling.

**Primary result (Black Summer, central scenario, PR=4.0 / FAR=0.752, AUD 10B damages)**:

| Entity | Type | USD M [5–95%] |
|--------|------|---------------|
| Former Soviet Union (1900–1991) | Nation State | 289 [227–360] |
| China (Coal, 1945–2004) | Nation State | 225 [176–279] |
| Saudi Aramco | State-owned | 139 [109–173] |
| Chevron | Investor-owned | 129 [101–160] |
| ExxonMobil | Investor-owned | 117 [92–146] |
| Gazprom | State-owned | 103 [80–128] |
| **Total Carbon Majors** | | **2,780** |

Uncertainty is the PR 5–95% bootstrap range. (The FaIR ensemble cancels in the warming *share*, so it contributes no liability spread.)

**Notebook**: `03-liability/01_black_summer_liability.ipynb`  
**Output**: `data/processed/black_summer_liability.parquet`  
**Wiki**: [[findings/2026-05-18-black-summer-liability]]

---

## Uncertainty Structure

Each step contributes uncertainty. Listed from largest to smallest contribution:

1. **Damage accounting** (~44× range): insured vs direct economic vs total social cost.
   The choice of damage framework matters far more than any attribution uncertainty.
2. **Scope 3 inclusion** (large per-entity impact): if courts exclude product combustion,
   per-entity liability shrinks substantially (scope-1 sensitivity in notebook 01-exploration/01).
3. **PR / FAR** (~1.6× across the bootstrap; ~larger across β choices): the FAR 5–95% bootstrap
   spans 0.59–0.93 for Black Summer; the choice of shift coefficient β (0.726 vs 0.935) moves PR
   from 4.0 to 5.2.
4. **Regional amplification (β)**: enters only through the PR via β (item 3), not as a separate
   liability multiplier.
5. **Entity warming share**: the FaIR ensemble cancels in the warming *share* (it is a ratio), so
   it contributes **no** liability uncertainty — liability spread comes entirely from PR and damages.

---

## Key Assumptions

- **Proportionality (TCRE)**: warming scales linearly with cumulative emissions. Valid to first
  order for CO₂; less so for methane and other short-lived climate forcers.
- **Proportional apportionment**: each entity's share of global warming = their share of the
  regional risk increase. This is the same basis used by Ekwurzel et al. (2017) and is standard
  in the climate attribution literature.
- **Physical ≠ legal**: these are risk-proportional estimates. Legal causation doctrines (but-for
  causation, substantial factor tests, market share liability) require separate analysis.
- **Carbon Majors coverage**: ~54% of total anthropogenic CO₂ (FFI + AFOLU). Total climate-attributed damages are larger than the Carbon Majors share computed here.

---

## Scalability

This pipeline is designed to scale to any climate event, not just Black Summer. The entity warming
shares (Steps 1–2) and Carbon Majors data are event-independent and reused across all events. For each new event, only Steps 3–6 need to be run:

1. **Damage data**: requires a reliable total-damage estimate. EM-DAT provides this at scale.
2. **ERA5 PR computation**: requires an ERA5 download for the relevant region and variable.
   Automated for any bounding box and event season.
3. **CMIP6 hist-nat**: streamed from pangeo for any region without local download.

The bottleneck is damage data quality, not the attribution science.
