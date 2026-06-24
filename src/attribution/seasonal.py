"""Seasonal series builders shared by the attribution notebooks."""

import numpy as np
import pandas as pd
import xarray as xr


def area_weighted_series(da: xr.DataArray) -> pd.Series:
    """Cosine-latitude weighted spatial mean of a (time, lat, lon) DataArray."""
    lat_dim = "latitude" if "latitude" in da.dims else "lat"
    lon_dim = "longitude" if "longitude" in da.dims else "lon"
    weights = np.cos(np.deg2rad(da[lat_dim])).broadcast_like(da)
    ts = da.weighted(weights).mean(dim=[lat_dim, lon_dim]).squeeze().to_series()
    ts.index = pd.to_datetime(ts.index)
    return ts.dropna()


def season_block_max(ts_monthly: pd.Series, months: list, shift_months: int = 9) -> pd.Series:
    """Cross-year seasonal maximum of a monthly series, indexed by season start year.

    Default shift (9) maps an Oct–Mar fire season onto the October year.
    Seasons truncated by the edges of the record are dropped — a block maximum
    over fewer months is biased low and contaminates the GEV fit.
    """
    s = ts_monthly[ts_monthly.index.month.isin(months)].copy()
    s.index = s.index - pd.DateOffset(months=shift_months)
    grouped = s.resample("YE")
    seasonal = grouped.max().dropna()
    complete = grouped.count() == len(months)
    seasonal = seasonal[complete.reindex(seasonal.index, fill_value=False)]
    seasonal.index = seasonal.index.year
    return seasonal


def wet_season_max_ndays(ts_daily: pd.Series, years: range, ndays: int = 7) -> pd.Series:
    """Max n-day rolling sum per wet season (Nov of year-1 through Apr of year)."""
    records = {}
    for yr in years:
        mask = ((ts_daily.index.year == yr - 1) & (ts_daily.index.month >= 11)) | (
            (ts_daily.index.year == yr) & (ts_daily.index.month <= 4)
        )
        season = ts_daily[mask]
        if len(season) < ndays:
            continue
        records[yr] = float(season.rolling(ndays).sum().max())
    return pd.Series(records)
