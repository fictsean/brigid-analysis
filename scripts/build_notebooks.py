"""Regenerate the attribution + liability notebooks as thin callers of
src/attribution, then execute them in place to refresh processed data.

Run from repo root:  .venv/bin/python scripts/build_notebooks.py
"""
import sys
from pathlib import Path

import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
from nbconvert.preprocessors import ExecutePreprocessor

ROOT = Path(__file__).resolve().parent.parent
NB = ROOT / "notebooks"


def build(path: Path, cells):
    nb = new_notebook()
    nb.cells = [
        new_markdown_cell(c[1]) if c[0] == "md" else new_code_cell(c[1])
        for c in cells
    ]
    nb.metadata = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"},
    }
    path.write_text(nbf.writes(nb))
    print(f"wrote {path.relative_to(ROOT)} ({len(cells)} cells)")
    return nb


def execute(path: Path, nb):
    ep = ExecutePreprocessor(timeout=1200, kernel_name="python3")
    ep.preprocess(nb, {"metadata": {"path": str(path.parent)}})
    path.write_text(nbf.writes(nb))
    print(f"executed {path.relative_to(ROOT)}")


# ─────────────────────────────────────────────────────────────────────────────
# Shared preamble for notebooks that live in notebooks/<dir>/<nb>.ipynb
PREAMBLE = """\
import warnings; warnings.filterwarnings('ignore')
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path('../../').resolve()
sys.path.insert(0, str(ROOT))
from src.attribution import (
    area_weighted_series, season_block_max, wet_season_max_ndays,
    load_gmst, extrapolate_to, smoothed_covariate, event_gmst_sigma,
    shift_fit_gev, fit_gev, build_liability_table, far,
    AUD_TO_USD, CC_RATE_STANDARD, CC_RATE_HIGH, CLIM_START, CLIM_END,
)
from scipy.stats import genextreme

sns.set_theme(style='whitegrid', palette='muted')
plt.rcParams['figure.dpi'] = 110
RAW  = ROOT / 'data' / 'raw'
PROC = ROOT / 'data' / 'processed'
FIGS = ROOT / 'outputs' / 'figures'
FIGS.mkdir(parents=True, exist_ok=True)
print('Setup complete.')
"""

# ═════════════════════════════════════════════════════════════════════════════
# 04 — Black Summer PR (shift-fit GEV)
# ═════════════════════════════════════════════════════════════════════════════
bs_pr = [
    ("md", """\
# Black Summer 2019–20 — Probability Ratio (nonstationary GEV shift-fit)

Replaces the earlier "detrended ERA5 + CMIP6 hist-nat" approach. The counterfactual
is now built from the **observed ERA5 record itself**, rescaled to a pre-industrial
climate using a GMST covariate (WWA-style shift fit), with a **GEV** tail fitted to
the seasonal block maxima.

- **P1 (factual)**: each season's fire-season (Oct–Mar) max of monthly-mean daily-max
  temperature, rescaled to the 2019 climate.
- **P0 (counterfactual)**: the same pool rescaled to the pre-industrial covariate (GMST = 0
  vs 1850–1900). The shift coefficient is the regional warming response β (°C local per °C global).
- **Primary β = 0.726** (ERA5-observed fire-season amplification, notebook 05). Sensitivities:
  CMIP6 annual-tas amplification (0.935) and a data-driven fitted β.

No CMIP6 streaming is required for the PR — the method is fully reproducible from local
ERA5 + the FaIR GMST parquet. CMIP6 hist-nat (notebook 03) remains a documented null-result
cross-check only."""),
    ("code", PREAMBLE),
    ("code", """\
# ── Region / season ──
LAT_S, LAT_N = -44, -28
LON_W, LON_E = 138, 154
FIRE_MONTHS  = [10, 11, 12, 1, 2, 3]
EVENT_YEAR   = 2019
ERA5_PATH = RAW / 'era5' / 'era5_mx2t_daily_se_australia_1961_2020.nc'

ds = xr.open_dataset(ERA5_PATH)
var = next(v for v in ['mx2t', 'maximum_2m_temperature'] if v in ds) \
      if any(v in ds for v in ['mx2t', 'maximum_2m_temperature']) else list(ds.data_vars)[0]
ts_daily = area_weighted_series(ds[var])
if ts_daily.mean() > 100:
    ts_daily = ts_daily - 273.15

# Fire-season block maxima of monthly-mean daily-max (matches CMIP6 tasmax definition),
# anomaly vs 1961–1990. Incomplete edge seasons are dropped inside season_block_max.
fire_season = season_block_max(ts_daily.resample('ME').mean(), FIRE_MONTHS)
anom = fire_season - fire_season.loc[CLIM_START:CLIM_END].mean()
print(f'Fire-season anomaly pool: {len(anom)} complete seasons '
      f'({anom.index.min()}–{anom.index.max()})')
print(f'{EVENT_YEAR} anomaly: {anom.loc[EVENT_YEAR]:.3f} °C  '
      f'(exceeded by {(anom > anom.loc[EVENT_YEAR]).sum()} seasons)')
print('Top 5 seasons:', {int(k): round(v, 2) for k, v in anom.nlargest(5).items()})
"""),
    ("code", """\
# ── GMST covariate (FaIR p50, smoothed) and event-year uncertainty ──
gmst = load_gmst(PROC)
covariate = smoothed_covariate(gmst['t_p50'])           # anomaly vs 1850–1900
g_sigma   = event_gmst_sigma(gmst, EVENT_YEAR)
print(f'GMST({EVENT_YEAR}) smoothed = {covariate.loc[EVENT_YEAR]:.3f} °C vs pre-industrial '
      f'(±{g_sigma:.3f} 1σ from FaIR)')

# ── Regional warming response β (°C local per °C global) ──
obs_af   = pd.read_csv(PROC / 'observed_amplification_factor.csv')
BETA_OBS = float(obs_af.set_index('source').loc['ERA5_observed', 'amplification'])   # 0.726
au_af    = pd.read_csv(PROC / 'au_amplification_factor.csv')
BETA_CMIP6 = float(au_af['amplification'].median())                                  # 0.935 (annual tas)
print(f'β primary (ERA5 fire-season amplification): {BETA_OBS:.3f}')
print(f'β sensitivity (CMIP6 annual-tas amplification): {BETA_CMIP6:.3f}')
"""),
    ("code", """\
# ── Shift-fit PR: primary (β=0.726) + sensitivities ──
methods = {
    'primary (β=0.726, ERA5 obs)': dict(beta=BETA_OBS),
    'sens (β=0.935, CMIP6 tas)':   dict(beta=BETA_CMIP6),
    'sens (β fitted, data-driven)': dict(beta=None),
}
results = {}
for name, kw in methods.items():
    r = shift_fit_gev(anom, covariate, EVENT_YEAR, mode='additive',
                      g_event_sigma=g_sigma, **kw)
    results[name] = r
    print(f'{name:32s}: {r.summary()}')

primary = results['primary (β=0.726, ERA5 obs)']
print(f'\\nPRIMARY  PR = {primary.pr:.2f} [{primary.pr_p05:.2f}–{primary.pr_p95:.2f}]  '
      f'FAR = {primary.far:.3f}')
print('WWA validation reference: FWI PR ≥ 4 (FAR ≥ 0.75), MSR PR ≥ 9 — '
      'van Oldenborgh et al. (2021)')
"""),
    ("code", """\
# ── Persist PR table + bootstrap samples ──
rows = []
for name, r in results.items():
    rows.append({'method': name, 'beta': r.beta, 'pr': r.pr,
                 'pr_p05': r.pr_p05, 'pr_p95': r.pr_p95, 'far': r.far,
                 'gev_xi': -r.gev_params[0]})
rows.append({'method': 'WWA FWI (van Oldenborgh 2021)', 'beta': np.nan, 'pr': 4.0,
             'pr_p05': 4.0, 'pr_p95': np.nan, 'far': 0.75, 'gev_xi': np.nan})
pr_df = pd.DataFrame(rows)
pr_df.to_csv(PROC / 'black_summer_pr_era5.csv', index=False)
pd.DataFrame({'pr_boot': primary.pr_boot}).to_parquet(
    PROC / 'black_summer_pr_shiftfit_bootstrap.parquet', index=False)
print('Saved black_summer_pr_era5.csv and black_summer_pr_shiftfit_bootstrap.parquet')
print(pr_df.to_string(index=False))
"""),
    ("code", """\
# ── Figure: distributions + PR vs threshold ──
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
xi, loc, scale = primary.gev_params
x = np.linspace(anom.min() - 0.5, anom.max() + 1.0, 300)
shift = primary.beta * covariate.loc[EVENT_YEAR]

ax = axes[0]
ax.hist(anom.values, bins=16, density=True, alpha=0.35, color='#90A4AE',
        label='ERA5 seasons (raw)')
ax.plot(x, genextreme.pdf(x, xi, loc, scale), color='#FF5722', lw=2.5,
        label='P1 factual GEV (2019 climate)')
ax.plot(x, genextreme.pdf(x, xi, loc - shift, scale), color='#2196F3', lw=2.5,
        label='P0 counterfactual GEV (pre-industrial)')
ax.axvline(primary.threshold, color='k', ls='--', lw=1.5,
           label=f'2019 event ({primary.threshold:.2f}°C)')
ax.set_xlabel('Fire-season max tasmax anomaly (°C)')
ax.set_ylabel('Density')
ax.set_title('Shift-fit GEV: factual vs counterfactual', fontsize=11)
ax.legend(fontsize=8)

ax2 = axes[1]
boot = primary.pr_boot
boot = boot[np.isfinite(boot)]
ax2.hist(np.clip(boot, 0, 30), bins=40, density=True, alpha=0.7, color='#673AB7')
ax2.axvline(primary.pr, color='k', lw=2, ls='--', label=f'median PR = {primary.pr:.1f}')
ax2.axvline(4.0, color='grey', lw=1.2, ls=':', label='WWA FWI lower bound (PR=4)')
ax2.set_xlabel('Probability Ratio')
ax2.set_title('Bootstrap PR distribution (β=0.726)', fontsize=11)
ax2.legend(fontsize=8)
plt.tight_layout()
plt.savefig(FIGS / 'black_summer_pr_shiftfit.png', bbox_inches='tight')
plt.show()
print('Saved figure.')
"""),
]

# ═════════════════════════════════════════════════════════════════════════════
# 07 — QLD floods PR (multiplicative shift-fit GEV)
# ═════════════════════════════════════════════════════════════════════════════
qld_pr = [
    ("md", """\
# 2022 SE QLD Floods — Probability Ratio (multiplicative GEV shift-fit)

Precipitation analogue of notebook 04. The counterfactual rescales each wet-season
7-day-max precipitation total to a pre-industrial climate **multiplicatively** (log-space
shift), with a GEV fitted to the block maxima.

- **Metric**: wet-season (Nov–Apr) maximum 7-day rolling precip, area-weighted over SE QLD.
- **Shift coefficient** β = d(log precip)/d(GMST) = ln(1+CC_rate)·α_QLD.
- **Primary**: CC 7%/°C × α_QLD = 0.289 (ERA5-observed wet-season Tmax) — a conservative
  lower bound. Sensitivities: CMIP6 α_QLD = 0.882, and dynamic 14%/°C.

A data-driven fitted β is also reported but is **not** used: the SE QLD wet-season precip
record is ENSO-dominated, and the fitted slope (~0.28, i.e. 28%/°C) reflects internal
variability, not a forced thermodynamic response."""),
    ("code", PREAMBLE),
    ("code", """\
# ── Region / season ──
LAT_S, LAT_N = -30, -24
LON_W, LON_E = 150, 154
WET_MONTHS = [11, 12, 1, 2, 3, 4]
EVENT_YEAR = 2022
ERA5_TP_PATH = RAW / 'era5' / 'era5_tp_daily_se_qld_1961_2022.nc'

ds_tp = xr.open_dataset(ERA5_TP_PATH)
if 'valid_time' in ds_tp.coords and 'time' not in ds_tp.dims:
    ds_tp = ds_tp.rename({'valid_time': 'time'})
tp_var = next(v for v in ds_tp.data_vars if 'tp' in v.lower() or 'precip' in v.lower())
da_tp = ds_tp[tp_var]

# ERA5 tp: 1-hour accumulation (m), sampled 4×/day. Sum to daily and scale to mm/day.
# The scale factor is common to all seasons, so it cancels in the multiplicative PR.
n_expected = 62 * len(WET_MONTHS) * 31
n_per_day  = da_tp.time.size / n_expected
da_daily   = da_tp.resample(time='1D').sum() * (24 / n_per_day) * 1000
ts_tp = area_weighted_series(da_daily)

ws = wet_season_max_ndays(ts_tp, range(CLIM_START + 1, EVENT_YEAR + 1), ndays=7)
rank = sorted(ws.values, reverse=True).index(ws[EVENT_YEAR]) + 1
print(f'Wet-season 7-day-max precip: {len(ws)} seasons')
print(f'{EVENT_YEAR} = {ws[EVENT_YEAR]:.1f} mm  (rank {rank}/{len(ws)})')
"""),
    ("code", """\
# ── GMST covariate (extrapolated to 2022, FaIR ends 2021) ──
gmst = load_gmst(PROC)
covariate = smoothed_covariate(extrapolate_to(gmst['t_p50'], EVENT_YEAR))
g_sigma   = event_gmst_sigma(gmst, EVENT_YEAR)
print(f'GMST({EVENT_YEAR}) = {covariate.loc[EVENT_YEAR]:.3f} °C vs pre-industrial (±{g_sigma:.3f})')

# ── α_QLD and shift coefficients β_log = ln(1+CC)·α ──
qld_af  = pd.read_csv(PROC / 'qld_amplification_factor.csv').set_index('model')
if 'ERA5_observed' not in qld_af.index:
    raise KeyError(
        "qld_amplification_factor.csv is missing the 'ERA5_observed' row (α=0.289) — the PRIMARY "
        "α_QLD for this notebook. It is not recomputed here; notebook 06's save cell preserves it. "
        "Rerun notebook 06 (which now preserves the row) or restore it. "
        "See wiki/findings/2026-06-17-lei-dropna-fix.md."
    )
A_ERA5  = float(qld_af.loc['ERA5_observed', 'amplification'])     # 0.289
A_CMIP6 = float(qld_af.drop(index='ERA5_observed')['amplification'].median())  # 0.882
beta = lambda cc, a: float(np.log(1 + cc) * a)
print(f'α_QLD ERA5-observed = {A_ERA5:.3f};  α_QLD CMIP6 median = {A_CMIP6:.3f}')
"""),
    ("code", """\
# ── Multiplicative shift-fit PR ──
methods = {
    'primary (CC 7%/°C × α=0.289)':  beta(CC_RATE_STANDARD, A_ERA5),
    'sens (CC 7%/°C × α=0.882 CMIP6)': beta(CC_RATE_STANDARD, A_CMIP6),
    'sens (CC 14%/°C × α=0.289)':    beta(CC_RATE_HIGH, A_ERA5),
    'sens (β fitted, ENSO-contaminated)': None,
}
results = {}
for name, b in methods.items():
    r = shift_fit_gev(ws, covariate, EVENT_YEAR, mode='multiplicative',
                      beta=b, g_event_sigma=g_sigma)
    results[name] = r
    tag = f'(fitted β={r.beta:.3f})' if b is None else f'(β={r.beta:.4f})'
    print(f'{name:36s}: PR={r.pr:.2f} [{r.pr_p05:.2f}–{r.pr_p95:.2f}] FAR={r.far:.3f} {tag}')

primary = results['primary (CC 7%/°C × α=0.289)']
print(f'\\nPRIMARY  PR = {primary.pr:.2f} [{primary.pr_p05:.2f}–{primary.pr_p95:.2f}]  '
      f'FAR = {primary.far:.3f}  (conservative lower bound)')
"""),
    ("code", """\
# ── Persist PR table + bootstrap ──
rows = [{'method': n, 'beta': r.beta, 'pr': r.pr, 'pr_p05': r.pr_p05,
         'pr_p95': r.pr_p95, 'far': r.far, 'gev_xi': -r.gev_params[0]}
        for n, r in results.items()]
pr_df = pd.DataFrame(rows)
pr_df.to_csv(PROC / 'qld_floods_pr_era5.csv', index=False)
pd.DataFrame({'pr_boot': primary.pr_boot}).to_parquet(
    PROC / 'qld_floods_pr_shiftfit_bootstrap.parquet', index=False)
print('Saved qld_floods_pr_era5.csv and qld_floods_pr_shiftfit_bootstrap.parquet')
print(pr_df.to_string(index=False))
"""),
    ("code", """\
# ── Figure ──
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
xi, loc, scale = primary.gev_params
factor = np.exp(primary.beta * covariate.loc[EVENT_YEAR])
x = np.linspace(ws.min() * 0.6, ws.max() * 1.1, 300)

ax = axes[0]
ax.hist(ws.values, bins=16, density=True, alpha=0.35, color='#90A4AE', label='ERA5 seasons')
ax.plot(x, genextreme.pdf(x, xi, loc, scale), color='#2196F3', lw=2.5,
        label='P1 factual GEV (2022)')
ax.plot(x, genextreme.pdf(x, xi, loc / factor, scale / factor), color='#4CAF50', lw=2.5,
        label='P0 counterfactual GEV')
ax.axvline(primary.threshold, color='k', ls='--', lw=1.5,
           label=f'2022 event ({primary.threshold:.0f} mm)')
ax.set_xlabel('Wet-season 7-day-max precip (mm)')
ax.set_ylabel('Density')
ax.set_title('Multiplicative shift-fit GEV', fontsize=11)
ax.legend(fontsize=8)

ax2 = axes[1]
boot = primary.pr_boot; boot = boot[np.isfinite(boot)]
ax2.hist(np.clip(boot, 0, 5), bins=40, density=True, alpha=0.7, color='#673AB7')
ax2.axvline(primary.pr, color='k', lw=2, ls='--', label=f'median PR = {primary.pr:.2f}')
ax2.axvline(1.0, color='grey', lw=1, ls=':')
ax2.set_xlabel('Probability Ratio')
ax2.set_title('Bootstrap PR distribution', fontsize=11)
ax2.legend(fontsize=8)
plt.tight_layout()
plt.savefig(FIGS / 'qld_floods_pr_shiftfit.png', bbox_inches='tight')
plt.show()
print('Saved figure.')
"""),
]

# ═════════════════════════════════════════════════════════════════════════════
# 05 — Observed amplification (legitimate part only; invalid PR×ratio removed)
# ═════════════════════════════════════════════════════════════════════════════
obs_amp = [
    ("md", """\
# SE Australia Observed Fire-Season Amplification (ERA5)

Computes the **fire-season warming response** β = (regional fire-season trend) / (global
GMST trend) from ERA5 — the physically meaningful coefficient used as the primary additive
shift in the Black Summer GEV shift-fit (notebook 04).

> **Methodology note.** A previous version of this notebook multiplied the Probability Ratio
> by an amplification *ratio* (`PR_obs = PR_era5 × α_obs/α_cmip6`). That is statistically
> invalid — PR is a nonlinear function of the distributional shift and does not scale
> linearly with an amplification ratio. The amplification factor enters correctly as the
> **shift coefficient β** inside the shift-fit (notebook 04), where β=0.726 is primary and
> β=0.935 is a sensitivity. The invalid `liability_obs_*` columns have been removed."""),
    ("code", PREAMBLE),
    ("code", """\
LAT_S, LAT_N = -44, -28
LON_W, LON_E = 138, 154
FIRE_MONTHS  = [10, 11, 12, 1, 2, 3]
TREND_START, TREND_END = 1961, 2020
from scipy.stats import linregress

ds = xr.open_dataset(RAW / 'era5' / 'era5_mx2t_daily_se_australia_1961_2020.nc')
ts_daily = area_weighted_series(ds['mx2t'])
if ts_daily.mean() > 100:
    ts_daily = ts_daily - 273.15

# Fire-season MEAN of daily max (trend metric, not block max)
ts_fs = ts_daily[ts_daily.index.month.isin(FIRE_MONTHS)].copy()
ts_fs.index = ts_fs.index - pd.DateOffset(months=9)
fire_season_mean = ts_fs.resample('YE').mean().dropna()
fire_season_mean.index = fire_season_mean.index.year
fs = fire_season_mean.loc[TREND_START:TREND_END]

slope_au = linregress(fs.index, fs.values).slope
ft = load_gmst(PROC)['t_p50'].loc[TREND_START:TREND_END]
slope_gl = linregress(ft.index, ft.values).slope
obs_amp = slope_au / slope_gl

print(f'ERA5 SE AU fire-season mean mx2t trend: {slope_au*10:.4f} °C/decade')
print(f'FaIR GMST trend:                        {slope_gl*10:.4f} °C/decade')
print(f'ERA5 observed fire-season amplification β = {obs_amp:.3f}')
"""),
    ("code", """\
# Persist (recomputed; matches prior value). Used as primary β in notebook 04.
out = pd.DataFrame([{
    'source': 'ERA5_observed',
    'trend_global_per_yr': slope_gl,
    'trend_au_per_yr': slope_au,
    'amplification': obs_amp,
    'period': f'{TREND_START}-{TREND_END}',
    'metric': 'fire_season_mean_mx2t',
}])
out.to_csv(PROC / 'observed_amplification_factor.csv', index=False)
print('Saved observed_amplification_factor.csv')
print(out.to_string(index=False))

print('\\nComparison of amplification estimates (all enter as the shift coefficient β):')
print(f'  ERA5 observed (fire-season mx2t):     {obs_amp:.3f}   ← PRIMARY')
au = pd.read_csv(PROC / 'au_amplification_factor.csv')
print(f'  CMIP6 ensemble (ANNUAL-mean tas):     {au[\"amplification\"].median():.3f}   ← sensitivity')
print('  NOTE: the CMIP6 value is an annual-mean tas amplification (notebook 02),')
print('  a different metric from the ERA5 fire-season value — they are not directly')
print('  comparable, which is why the fire-season ERA5 estimate is used as primary.')
"""),
    ("code", """\
# ── β-sensitivity of the Black Summer PR (the statistically valid use of α) ──
gmst = load_gmst(PROC)
covariate = smoothed_covariate(gmst['t_p50'])
g_sigma = event_gmst_sigma(gmst, 2019)
anom_fs = season_block_max(ts_daily.resample('ME').mean(), FIRE_MONTHS)
anom = anom_fs - anom_fs.loc[CLIM_START:CLIM_END].mean()

print('Black Summer PR as a function of the shift coefficient β:')
for label, b in [('ERA5 obs β=0.726 (PRIMARY)', obs_amp),
                 ('CMIP6 tas β=0.935', float(au['amplification'].median()))]:
    r = shift_fit_gev(anom, covariate, 2019, mode='additive', beta=b, g_event_sigma=g_sigma)
    print(f'  {label:28s}: PR={r.pr:.2f} [{r.pr_p05:.2f}–{r.pr_p95:.2f}]  FAR={r.far:.3f}')
print('\\nHigher β → larger counterfactual shift → higher PR. This is the correct,')
print('nonlinear dependence — not a linear PR×ratio scaling.')
"""),
]


# ═════════════════════════════════════════════════════════════════════════════
# 03-liability/01 — Black Summer liability (global-share apportionment)
# ═════════════════════════════════════════════════════════════════════════════
bs_liab = [
    ("md", """\
# Black Summer 2019–20 — Entity Liability

End-to-end liability with the **corrected apportionment convention**: each entity is charged
its share of **total** anthropogenic warming (`global_share`), not its share of the Carbon
Majors subtotal. The Carbon Majors collectively absorb ~75% of climate-attributed damages;
the rest is attributable to emitters outside the database.

- **PR/FAR**: nonstationary GEV shift-fit, primary PR ≈ 4.0, FAR ≈ 0.75 (notebook 04).
- **Uncertainty**: from the PR bootstrap (FaIR ensemble cancels in every warming *share*).
- **Damage scenarios** are the discrete damage axis; the same primary FAR is applied to each.
  A separate PR × damages grid shows the joint sensitivity."""),
    ("code", PREAMBLE),
    ("code", """\
ew = pd.read_parquet(PROC / 'entity_warming_contribution.parquet')
print(f'Carbon Majors coverage of global fossil CO2: {ew[\"global_share\"].sum()*100:.1f}%')

# PR from notebook 04 (primary) + bootstrap samples for FAR uncertainty
pr_df = pd.read_csv(PROC / 'black_summer_pr_era5.csv')
primary_row = pr_df[pr_df['method'].str.startswith('primary')].iloc[0]
PR_PRIMARY = float(primary_row['pr'])
boot = pd.read_parquet(PROC / 'black_summer_pr_shiftfit_bootstrap.parquet')['pr_boot'].values
print(f'Primary PR = {PR_PRIMARY:.2f}, FAR = {far(PR_PRIMARY):.3f}  '
      f'(bootstrap n={len(boot)})')

FX = AUD_TO_USD[2020]
scenarios = {
    'conservative':  dict(damages_usd_b=2.32 * FX,  pr=PR_PRIMARY, pr_samples=boot,
                          label='Insured losses (ICA), AUD 2.32B'),
    'central':       dict(damages_usd_b=10.0 * FX,  pr=PR_PRIMARY, pr_samples=boot,
                          label='Direct economic, AUD 10B'),
    'comprehensive': dict(damages_usd_b=103.0 * FX, pr=PR_PRIMARY, pr_samples=boot,
                          label='Total social cost, AUD 103B'),
}
"""),
    ("code", """\
liability, totals = build_liability_table(ew, scenarios)
liability.to_parquet(PROC / 'black_summer_liability.parquet', index=False)
totals.to_csv(PROC / 'black_summer_scenario_totals.csv', index=False)

print('Scenario totals (Carbon Majors, ~75% of global):')
print(totals[['scenario', 'damages_usd_b', 'far', 'far_p05', 'far_p95',
              'total_attributed_usd_b']].to_string(index=False))
print(f'\\nPRIMARY (central): USD {totals.set_index(\"scenario\").loc[\"central\",\"total_attributed_usd_b\"]:.2f}B '
      f'across Carbon Majors')
print('\\nTop 10 entities — central scenario (USD M, with 5–95% PR uncertainty):')
cols = ['rank', 'parent_entity', 'parent_type', 'liability_central_USD_M',
        'liability_central_p05_USD_M', 'liability_central_p95_USD_M']
top10 = liability.head(10)[cols].copy()
for c in cols[3:]:
    top10[c] = top10[c].map('{:,.1f}'.format)
print(top10.to_string(index=False))
"""),
    ("code", """\
# ── Figure: top-20 entities, central scenario with PR-uncertainty bars ──
top20 = liability.head(20)
type_colors = {'Investor-owned Company': '#2196F3', 'State-owned Entity': '#FF5722',
               'Nation State': '#4CAF50'}
colors = top20['parent_type'].map(type_colors).fillna('#9E9E9E')
fig, ax = plt.subplots(figsize=(11, 8))
y = np.arange(len(top20))
ax.barh(y, top20['liability_central_USD_M'], color=colors, alpha=0.85)
xerr_lo = (top20['liability_central_USD_M'] - top20['liability_central_p05_USD_M']).clip(lower=0)
xerr_hi = (top20['liability_central_p95_USD_M'] - top20['liability_central_USD_M']).clip(lower=0)
ax.errorbar(top20['liability_central_USD_M'], y, xerr=[xerr_lo, xerr_hi],
            fmt='none', color='#333', lw=1, capsize=3, alpha=0.6, label='PR 5–95% (bootstrap)')
ax.set_yticks(y); ax.set_yticklabels(top20['parent_entity'], fontsize=9); ax.invert_yaxis()
ax.set_xlabel('Attributed liability — central scenario (USD millions)')
ax.set_title('Black Summer 2019–20: entity liability\\n'
             'global warming share × FAR(0.75) × AUD 10B damages', fontsize=12)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(facecolor=c, label=t) for t, c in type_colors.items()] +
                  [Patch(facecolor='#333', label='PR 5–95% (bootstrap)')],
          fontsize=8, loc='lower right')
plt.tight_layout(); plt.savefig(FIGS / 'black_summer_liability_top20.png', bbox_inches='tight')
plt.show()
"""),
    ("code", """\
# ── Joint PR × damages sensitivity (Saudi Aramco) ──
aramco = float(liability.loc[liability['parent_entity'] == 'Saudi Aramco', 'global_share'].iloc[0])
pr_range = [2, 3, 4, 6, 9, 12]
dmg_aud  = [2.32, 5, 10, 25, 50, 103]
grid = pd.DataFrame(
    index=[f'PR={p}' for p in pr_range],
    columns=[f'AUD {d}B' for d in dmg_aud],
    data=[[aramco * far(p) * d * FX * 1000 for d in dmg_aud] for p in pr_range])
fig, ax = plt.subplots(figsize=(9, 5))
sns.heatmap(grid.astype(float), annot=True, fmt='.0f', cmap='YlOrRd',
            cbar_kws={'label': 'USD millions'}, linewidths=0.5, ax=ax)
ax.set_title('Saudi Aramco — Black Summer liability sensitivity (USD M)\\n'
             'global-share apportionment', fontsize=11)
ax.set_xlabel('Total damages'); ax.set_ylabel('Probability Ratio')
plt.tight_layout(); plt.savefig(FIGS / 'black_summer_sensitivity_aramco.png', bbox_inches='tight')
plt.show()
print(f'Saudi Aramco global warming share: {aramco*100:.3f}%')
print(f'Saudi Aramco central liability: USD '
      f'{liability.loc[liability.parent_entity==\"Saudi Aramco\",\"liability_central_USD_M\"].iloc[0]:.0f}M')
"""),
]

# ═════════════════════════════════════════════════════════════════════════════
# 03-liability/02 — QLD floods liability
# ═════════════════════════════════════════════════════════════════════════════
qld_liab = [
    ("md", """\
# 2022 SE QLD Floods — Entity Liability

Same corrected pipeline as Black Summer: **global-share** apportionment, PR/FAR from the
multiplicative GEV shift-fit (notebook 07), uncertainty from the PR bootstrap.

- **Primary PR ≈ 1.11, FAR ≈ 10%** (CC 7%/°C × α_QLD=0.289 — conservative lower bound).
- **Damage central AUD 10B remains a placeholder** pending an official QLD Treasury / Deloitte
  / NEMA figure; EM-DAT records a redacted value for REDACTED-DISNO, consistent with that order."""),
    ("code", PREAMBLE),
    ("code", """\
ew = pd.read_parquet(PROC / 'entity_warming_contribution.parquet')
print(f'Carbon Majors coverage: {ew[\"global_share\"].sum()*100:.1f}%')

pr_df = pd.read_csv(PROC / 'qld_floods_pr_era5.csv')
primary_row = pr_df[pr_df['method'].str.startswith('primary')].iloc[0]
PR_PRIMARY = float(primary_row['pr'])
boot = pd.read_parquet(PROC / 'qld_floods_pr_shiftfit_bootstrap.parquet')['pr_boot'].values
print(f'Primary PR = {PR_PRIMARY:.3f}, FAR = {far(PR_PRIMARY):.3f}  (bootstrap n={len(boot)})')

FX = AUD_TO_USD[2022]
scenarios = {
    'conservative':  dict(damages_usd_b=5.56 * FX, pr=PR_PRIMARY, pr_samples=boot,
                          label='ICA insured, AUD 5.56B'),
    'central':       dict(damages_usd_b=10.0 * FX, pr=PR_PRIMARY, pr_samples=boot,
                          label='Direct economic (placeholder), AUD 10B'),
    'comprehensive': dict(damages_usd_b=20.0 * FX, pr=PR_PRIMARY, pr_samples=boot,
                          label='Social cost (placeholder), AUD 20B'),
}
"""),
    ("code", """\
liability, totals = build_liability_table(ew, scenarios)
liability.to_parquet(PROC / 'qld_floods_liability.parquet', index=False)
totals.to_csv(PROC / 'qld_floods_scenario_totals.csv', index=False)

print('Scenario totals (Carbon Majors, ~75% of global):')
print(totals[['scenario', 'damages_usd_b', 'far', 'far_p05', 'far_p95',
              'total_attributed_usd_b']].to_string(index=False))
print('\\nTop 10 entities — central scenario (USD M):')
cols = ['rank', 'parent_entity', 'parent_type', 'liability_central_USD_M',
        'liability_central_p05_USD_M', 'liability_central_p95_USD_M']
top10 = liability.head(10)[cols].copy()
for c in cols[3:]:
    top10[c] = top10[c].map('{:,.2f}'.format)
print(top10.to_string(index=False))
ar = liability.loc[liability.parent_entity == 'Saudi Aramco']
print(f'\\nSaudi Aramco central: USD {ar[\"liability_central_USD_M\"].iloc[0]:.1f}M')
"""),
    ("code", """\
# ── Figure: PR × damages sensitivity grid (central uncertainty is small here) ──
aramco = float(liability.loc[liability['parent_entity'] == 'Saudi Aramco', 'global_share'].iloc[0])
pr_range = [1.1, 1.2, 1.4, 1.8, 2.5, 4.0]
dmg_aud  = [5.56, 10, 15, 20, 30, 50]
grid = pd.DataFrame(
    index=[f'PR={p}' for p in pr_range],
    columns=[f'AUD {d}B' for d in dmg_aud],
    data=[[aramco * far(p) * d * FX * 1000 for d in dmg_aud] for p in pr_range])
fig, ax = plt.subplots(figsize=(9, 5))
sns.heatmap(grid.astype(float), annot=True, fmt='.1f', cmap='YlOrRd',
            cbar_kws={'label': 'USD millions'}, linewidths=0.5, ax=ax)
ax.set_title('Saudi Aramco — 2022 QLD Floods liability sensitivity (USD M)', fontsize=11)
ax.set_xlabel('Total damages'); ax.set_ylabel('Probability Ratio')
plt.tight_layout(); plt.savefig(FIGS / 'qld_floods_sensitivity_aramco.png', bbox_inches='tight')
plt.show()
print(f'Aramco global warming share: {aramco*100:.3f}%')
"""),
]

if __name__ == "__main__":
    specs = [
        (NB / "02-attribution" / "04_black_summer_pr_era5.ipynb", bs_pr),
        (NB / "02-attribution" / "05_observed_amplification.ipynb", obs_amp),
        (NB / "02-attribution" / "07_qld_floods_pr_era5.ipynb", qld_pr),
        (NB / "03-liability" / "01_black_summer_liability.ipynb", bs_liab),
        (NB / "03-liability" / "02_qld_floods_liability.ipynb", qld_liab),
    ]
    targets = sys.argv[1:]
    for path, cells in specs:
        if targets and path.stem not in targets and not any(t in str(path) for t in targets):
            continue
        nb = build(path, cells)
        execute(path, nb)
    print("\\nAll done.")
