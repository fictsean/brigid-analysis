"""FaIR GMST covariate helpers.

The FaIR ensemble temperature (data/processed/fair_global_temperature.parquet)
is expressed as an anomaly relative to 1850–1900, so the pre-industrial
counterfactual covariate is exactly 0 — no baseline arithmetic needed.
"""

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import linregress

SMOOTH_WINDOW = 4  # years — WWA convention for the GMST covariate


def load_gmst(processed_dir: Path) -> pd.DataFrame:
    """Load the FaIR GMST percentile table indexed by year (anomaly vs 1850–1900)."""
    ft = pd.read_parquet(Path(processed_dir) / "fair_global_temperature.parquet")
    if "year" in ft.columns:
        ft = ft.set_index("year")
    return ft[["t_p05", "t_p50", "t_p95"]]


def extrapolate_to(series: pd.Series, target_year: int, fit_window: int = 12) -> pd.Series:
    """Extend a GMST series past its last year with a linear fit over the final window."""
    if target_year <= series.index.max():
        return series
    sub = series.loc[series.index.max() - fit_window + 1 :]
    slope, intercept, *_ = linregress(sub.index, sub.values)
    extra_years = range(int(series.index.max()) + 1, target_year + 1)
    extra = pd.Series({y: slope * y + intercept for y in extra_years})
    return pd.concat([series, extra])


def smoothed_covariate(gmst_p50: pd.Series, window: int = SMOOTH_WINDOW) -> pd.Series:
    """Centred running mean of GMST — the shift-fit covariate."""
    return gmst_p50.rolling(window, center=True, min_periods=1).mean()


def event_gmst_sigma(gmst: pd.DataFrame, year: int) -> float:
    """1-sigma uncertainty of the GMST level at `year` from the FaIR 5–95% range."""
    p05 = extrapolate_to(gmst["t_p05"], year).loc[year]
    p95 = extrapolate_to(gmst["t_p95"], year).loc[year]
    return float((p95 - p05) / (2 * 1.645))
