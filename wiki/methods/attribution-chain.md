---
type: method
name: attribution-chain
tags: [overview, attribution, liability, end-to-end]
related: [emissions-to-forcing, far-probability-ratio, regional-amplification, carbon-majors-database, era5-reanalysis, cmip6, ekwurzel-2017]
status: active
confidence: high
last_updated: 2026-05-24
---

# Attribution Chain — End-to-End Overview

This page describes the full methodology for calculating an entity's proportional liability for a
specific climate disaster. It is the entry point before reading the individual method pages or
notebooks. Terms in **bold** are defined on first use.

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

**Key result**: Carbon Majors collectively responsible for ~45% of observed 1.18°C warming.
Saudi Aramco: 44.7 m°C; ExxonMobil: 37.6 m°C (where m°C = millidegrees Celsius).

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
An α of 1.5 for a region means temperatures there rose 50% faster than the world average — so
each degree of global warming produced 1.5°C of local warming.

In our liability formula, entity warming shares are expressed as fractions of *regional* warming,
and because both the entity and the total scale by the same α, it cancels in the ratio. In
practice, **entity warming shares are used directly** in the liability formula without needing to
separately apply α. However, α matters indirectly: the climate models used for the counterfactual
(Step 4 below) should correctly represent how the region warms. If they over- or under-estimate α,
the counterfactual is biased.

**Current estimates for SE Australia (fire season)**:

| Source | α | What was measured |
|--------|---|-------------------|
| CMIP6 models (ACCESS-CM2 + ACCESS-ESM1-5) | 0.935 | Model fire-season daily-max temperature vs model global mean |
| ERA5 observed | 0.726 | Observed fire-season daily-max temperature vs modelled global mean (FaIR) |

Both values are below 1.0, meaning SE Australia's fire-season temperatures warmed slightly slower
than the global average over this period and metric. Note that BoM (Australian Bureau of Meteorology)
reports annual mean temperatures in SE Australia warming ~1.3–1.5× faster than the global average
since 1910 — that's a different metric (annual mean since 1910 vs fire-season daily maximum since
1961), which is why the numbers differ.

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
climate model variable called **tasmax** (daily maximum near-surface air temperature). We compute
the fire-season (October–March) anomaly for SE Australia.

### Counterfactual distribution (P0)

We use **CMIP6 hist-nat** runs. CMIP6 (Coupled Model Intercomparison Project Phase 6) is the
coordinated global effort to run climate models under standardised conditions. The **hist-nat**
(historical natural-only) experiment runs the same models as the standard historical simulation
but removes all human-caused forcing (no fossil fuel CO₂, no land-use change, no aerosols) —
only natural factors like volcanic eruptions and changes in solar output are included. This
is our best estimate of what the climate would have looked like without human influence.

We fit a statistical distribution (Gaussian) to both P1 and P0, compute PR at the observed event
severity, and repeat 2,000 times with bootstrapped samples to get an uncertainty range.

**Why ERA5 for P1 (not a climate model)**: Climate models can have biases in how they represent
regional warming. Using ERA5 for P1 means the factual climate is the actual observed record, not
a model's version of it. This is the standard approach used by the World Weather Attribution
(WWA) group.

**Why not use WWA's published results directly**: WWA publishes attribution studies for major
events, but only ~50 events have been studied, and coverage is uneven. Computing our own ERA5
+ hist-nat PR keeps the pipeline traceable and scalable to any event.

**Primary result for Black Summer**: PR = 1.80 [1.00–2.86] (bootstrap median and 5th–95th
percentile range, 4-model corrected run). FAR = 44.4%. At the 99th percentile threshold,
PR = 3.3. This is a conservative lower bound — the 4 available hist-nat models overestimate
SE Australian natural variability. WWA (PR ≥ 4–9) is the better-constrained upper reference.

**Notebooks**: `02-attribution/04_black_summer_pr_era5.ipynb` (primary),
`02-attribution/03_black_summer_pr_cmip6.ipynb` (null result — CMIP6 hist vs hist-nat gave PR=0.6)  
**Output**: `data/processed/black_summer_pr_era5.csv`, `black_summer_pr_era5_bootstrap.parquet`  
**Wiki**: [[methods/far-probability-ratio]], [[findings/2026-05-24-black-summer-pr-era5]],
[[datasets/wwa-studies]]

---

## Step 5 — FAR × Damages → Climate-Attributed Damages

FAR is multiplied by a total damage estimate for the event. The interpretation: FAR% of the
damages would not have occurred in a world without anthropogenic climate change.

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

The final step combines the entity's global warming share (Step 2), the FAR (Step 4), and the
total damage estimate (Step 5).

```
entity_liability_USD = entity_warming_share × FAR × total_damages_USD
```

The proportionality assumption: if entity X caused W% of global warming, they caused W% of the
regional climate change signal, and therefore W% of the climate-attributed fraction of damages.
This is a physical-science proportionality claim, not a legal ruling.

**Primary result (Black Summer, central scenario)**:

| Entity | Type | USD M |
|--------|------|-------|
| Saudi Aramco | State-owned | 261 |
| ExxonMobil | Investor-owned | 219 |
| Gazprom | State-owned | 192 |
| BP | Investor-owned | 167 |
| Shell | Investor-owned | 159 |
| **Total Carbon Majors** | | **3,067** |

**Notebook**: `03-liability/01_black_summer_liability.ipynb`  
**Output**: `data/processed/black_summer_liability.parquet`  
**Wiki**: [[findings/2026-05-18-black-summer-liability]]

---

## Uncertainty Structure

Each step contributes uncertainty. Listed from largest to smallest contribution:

1. **Damage accounting** (~120× range): insured vs direct economic vs total social cost.
   The choice of damage framework matters far more than any attribution uncertainty.
2. **PR / FAR** (~3× within defensible ERA5 range): driven by limited hist-nat model availability
   and natural variability in the observed record. Comparing ERA5 median (1.80) to ERA5 99th-pct
   (3.3) to WWA (≥4–9) spans the current scientifically defensible range.
3. **Scope 3 inclusion** (~9× impact on per-entity figures): if courts exclude product combustion,
   entity liability shrinks approximately 9×.
4. **Entity warming share** (<2× from p05 to p95): FaIR ensemble uncertainty is relatively small.
5. **Regional amplification** (~20% effect): the difference between CMIP6 α (0.935) and ERA5 α
   (0.726) shifts the obs-corrected central liability from 3.07B to 1.96B.

---

## Key Assumptions

- **Proportionality (TCRE)**: warming scales linearly with cumulative emissions. Valid to first
  order for CO₂; less so for methane and other short-lived climate forcers.
- **Proportional apportionment**: each entity's share of global warming = their share of the
  regional risk increase. This is the same basis used by Ekwurzel et al. (2017) and is standard
  in the climate attribution literature.
- **Physical ≠ legal**: these are risk-proportional estimates. Legal causation doctrines (but-for
  causation, substantial factor tests, market share liability) require separate analysis.
- **Carbon Majors coverage**: ~45% of total global fossil CO₂. Total climate-attributed damages
  are larger than the Carbon Majors share computed here.

---

## Scalability

This pipeline is designed to scale to any climate event, not just Black Summer. The entity warming
shares (Steps 1–2) and Carbon Majors data are event-independent and reused across all events. For
each new event, only Steps 3–6 need to be run:

1. **Damage data**: requires a reliable total-damage estimate. EM-DAT provides this at scale.
2. **ERA5 PR computation**: requires an ERA5 download for the relevant region and variable.
   Automated for any bounding box and event season.
3. **CMIP6 hist-nat**: streamed from pangeo for any region without local download.

The bottleneck is damage data quality, not the attribution science.
