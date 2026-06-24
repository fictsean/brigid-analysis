"""WWA-style nonstationary shift-fit event attribution with a GEV tail.

Replaces the earlier "detrended ERA5" implementation, which had two problems:

1. It removed only the warming since the 1961–1990 baseline (not since
   pre-industrial) and fitted the factual distribution to the trended
   1961–2020 pool, mixing climates on both sides of the ratio.
2. It evaluated Gaussian/log-normal tails at or near the record maximum,
   where the parametric form dominates the answer; seasonal block maxima
   call for a GEV.

Here every year in the observed pool is rescaled to a common climate using a
GMST covariate (FaIR anomaly vs 1850–1900, so the pre-industrial counterfactual
covariate is exactly 0):

  factual pool        x1_t = transform(x_t, g_t -> g_event)
  counterfactual pool x0_t = transform(x_t, g_t -> 0)

A GEV is fitted to the factual pool; the counterfactual differs only by the
(additive or multiplicative) climate shift, so its exceedance probability is
evaluated from the same fit with a shifted threshold. PR = P1/P0 at the
observed event magnitude. Bootstrap resamples years (and, if requested,
refits beta and perturbs the event-year GMST) to propagate sampling and
covariate uncertainty jointly.
"""

from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from scipy.stats import genextreme, linregress

from .constants import GEV_SHAPE_BOUNDS


def fit_gev(values: np.ndarray, shape_bounds: tuple = GEV_SHAPE_BOUNDS):
    """Fit a GEV, constraining the shape ξ to `shape_bounds` (WWA practice).

    scipy's genextreme parameterises with c = -ξ, so the bounds flip sign.
    Returns (c, loc, scale).
    """
    c, loc, scale = genextreme.fit(values)
    xi = -c
    lo, hi = shape_bounds
    if not (lo <= xi <= hi):
        xi_clipped = float(np.clip(xi, lo, hi))
        c, loc, scale = genextreme.fit(values, f0=-xi_clipped)
    return c, loc, scale


def _fit_beta(values: np.ndarray, covariate: np.ndarray, mode: str) -> float:
    """OLS slope of the response on the GMST covariate.

    additive       : beta = d(x)/dg      (°C of block-max per °C GMST)
    multiplicative : beta = d(log x)/dg   (fractional change per °C GMST)
    """
    response = np.log(values) if mode == "multiplicative" else values
    slope, *_ = linregress(covariate, response)
    return float(slope)


@dataclass
class ShiftFitResult:
    pr: float
    far: float
    p1: float
    p0: float
    beta: float
    threshold: float
    gev_params: tuple          # (c, loc, scale) of the factual fit
    pr_boot: np.ndarray = field(default=None, repr=False)
    pr_p05: float = np.nan
    pr_p95: float = np.nan
    far_p05: float = np.nan
    far_p95: float = np.nan
    n_boot_degenerate: int = 0

    def summary(self) -> str:
        return (
            f"PR = {self.pr:.2f} [{self.pr_p05:.2f}–{self.pr_p95:.2f}]  "
            f"FAR = {self.far:.3f} [{self.far_p05:.3f}–{self.far_p95:.3f}]  "
            f"beta = {self.beta:.3f}  GEV(xi={-self.gev_params[0]:.3f}, "
            f"loc={self.gev_params[1]:.3f}, scale={self.gev_params[2]:.3f})"
        )


def _far(pr: float) -> float:
    return 1.0 - 1.0 / pr if pr > 1 else 0.0


def shift_fit_gev(
    values: pd.Series,
    covariate: pd.Series,
    event_year: int,
    mode: str = "additive",
    beta: float = None,
    counterfactual_g: float = 0.0,
    n_boot: int = 2000,
    seed: int = 42,
    g_event_sigma: float = 0.0,
    shape_bounds: tuple = GEV_SHAPE_BOUNDS,
) -> ShiftFitResult:
    """Shift-fit GEV attribution for one event.

    Parameters
    ----------
    values : seasonal block maxima (anomalies or absolute), indexed by season year.
    covariate : smoothed GMST anomaly vs 1850–1900, indexed by year (superset of
        values.index). Pre-industrial counterfactual covariate = 0.
    event_year : season year of the event; values[event_year] is the threshold.
    mode : 'additive' (temperature: x shifts by beta·Δg per °C GMST) or
        'multiplicative' (precipitation: x scales by exp(beta·Δg), so beta is
        d(log x)/dg — the fractional change per °C GMST, e.g. ln(1+CC_rate)·alpha).
    beta : prescribed scaling. If None, fitted by OLS of the response (x, or
        log x for multiplicative) on the covariate and refitted in every
        bootstrap iteration.
    g_event_sigma : 1-sigma uncertainty on the event-year GMST level (FaIR);
        sampled in the bootstrap.
    """
    values = values.dropna()
    g = covariate.reindex(values.index).values
    x = values.values.astype(float)
    g_event = float(covariate.loc[event_year])
    threshold = float(values.loc[event_year])

    fitted_beta = beta is None
    if fitted_beta:
        beta = _fit_beta(x, g, mode)

    def transform(xv, gv, g_target, b):
        if mode == "additive":
            return xv + b * (g_target - gv)
        if mode == "multiplicative":
            return xv * np.exp(b * (g_target - gv))
        raise ValueError(f"unknown mode {mode!r}")

    def pr_once(xv, gv, b, g_evt):
        x1 = transform(xv, gv, g_evt, b)
        params = fit_gev(x1, shape_bounds)
        p1 = float(genextreme.sf(threshold, *params))
        # x0 = x1 transformed from g_evt back to the counterfactual climate.
        # Equivalently, evaluate the factual fit at the threshold mapped forward.
        if mode == "additive":
            thr0 = threshold + b * (g_evt - counterfactual_g)
        else:
            thr0 = threshold * np.exp(b * (g_evt - counterfactual_g))
        p0 = float(genextreme.sf(thr0, *params))
        return p1, p0, params

    p1, p0, params = pr_once(x, g, beta, g_event)
    pr_point = p1 / p0 if p0 > 0 else np.inf

    rng = np.random.default_rng(seed)
    boot, degenerate = [], 0
    n = len(x)
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        xb, gb = x[idx], g[idx]
        b = _fit_beta(xb, gb, mode) if fitted_beta else beta
        g_evt = g_event + rng.normal(0, g_event_sigma) if g_event_sigma > 0 else g_event
        try:
            p1b, p0b, _ = pr_once(xb, gb, b, g_evt)
        except Exception:
            degenerate += 1
            continue
        if p1b <= 0 and p0b <= 0:
            degenerate += 1
            continue
        boot.append(p1b / p0b if p0b > 0 else np.inf)

    boot = np.array(boot)
    pr_med = float(np.median(boot)) if len(boot) else np.nan
    # np.percentile handles inf naturally: p95 is only inf if >5% of samples are
    # inf (i.e. the event is essentially impossible in the counterfactual).
    pr_p05 = float(np.percentile(boot, 5)) if len(boot) else np.nan
    pr_p95 = float(np.percentile(boot, 95)) if len(boot) else np.nan

    return ShiftFitResult(
        pr=pr_med if np.isfinite(pr_med) else pr_point,
        far=_far(pr_med if np.isfinite(pr_med) else pr_point),
        p1=p1,
        p0=p0,
        beta=float(beta),
        threshold=threshold,
        gev_params=params,
        pr_boot=boot,
        pr_p05=pr_p05,
        pr_p95=pr_p95,
        far_p05=_far(pr_p05),
        far_p95=_far(pr_p95) if np.isfinite(pr_p95) else 1.0,
        n_boot_degenerate=degenerate,
    )
