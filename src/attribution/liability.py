"""Entity liability tables from warming shares, PR/FAR, and damage scenarios.

Apportionment convention (global share)
---------------------------------------
Each entity is charged its share of TOTAL anthropogenic warming, not its share
of the Carbon Majors subtotal:

    liability_entity = global_warming_share_entity × FAR × total_damages

Under TCRE proportionality the warming share equals the emissions share
(entity cumulative CO2e / global cumulative *total* anthropogenic CO2 (FFI +
AFOLU) — the FaIR ΔT cancels in the ratio), so `global_share` from
entity_warming_contribution.parquet is used directly. The Carbon Majors
collectively absorb ~54% of climate-attributed damages (Stuart-Smith et al.
2025 benchmark); the remainder is attributable to emitters outside the database.

Uncertainty convention
----------------------
FaIR ensemble uncertainty cancels in every share ratio (warming_pXX is
global_share × ΔT_pXX, so normalising removes ΔT entirely). Liability
uncertainty therefore comes from the PR bootstrap (5th–95th percentile of
FAR), propagated per scenario. Damage-accounting uncertainty is expressed as
discrete scenarios, not percentiles.
"""

import numpy as np
import pandas as pd


def far(pr: float) -> float:
    """Fraction of Attributable Risk from a Probability Ratio."""
    return 1.0 - 1.0 / pr if pr > 1 else 0.0


def build_liability_table(entity_warming: pd.DataFrame, scenarios: dict):
    """Build per-entity liability and scenario totals.

    Parameters
    ----------
    entity_warming : entity_warming_contribution.parquet contents; must contain
        parent_entity, parent_type, global_share, warming_p50_degC.
    scenarios : {name: {'damages_usd_b': float, 'pr': float,
                        'pr_samples': np.ndarray or None, 'label': str}}
        pr is the central (median) PR; pr_samples, when given, is the bootstrap
        sample used for the 5–95% liability range.

    Returns
    -------
    (liability_df, scenario_totals_df)
    """
    lb = entity_warming[
        ["parent_entity", "parent_type", "global_share", "warming_p50_degC"]
    ].copy()
    # Within-Carbon-Majors share, for reference/plots only — NOT used for liability.
    lb["cm_warming_share"] = lb["global_share"] / lb["global_share"].sum()

    totals = []
    for name, sc in scenarios.items():
        d = sc["damages_usd_b"]
        f_med = far(sc["pr"])
        lb[f"liability_{name}_USD_M"] = lb["global_share"] * f_med * d * 1000

        f05 = f95 = None
        samples = sc.get("pr_samples")
        if samples is not None and len(samples):
            fars = np.array([far(p) for p in np.asarray(samples)])
            f05, f95 = np.percentile(fars, [5, 95])
            lb[f"liability_{name}_p05_USD_M"] = lb["global_share"] * f05 * d * 1000
            lb[f"liability_{name}_p95_USD_M"] = lb["global_share"] * f95 * d * 1000

        totals.append(
            {
                "scenario": name,
                "label": sc.get("label", name),
                "damages_usd_b": d,
                "pr": sc["pr"],
                "far": f_med,
                "far_p05": f05,
                "far_p95": f95,
                "cm_coverage_share": lb["global_share"].sum(),
                "total_attributed_usd_b": float(lb[f"liability_{name}_USD_M"].sum()) / 1000,
            }
        )

    sort_col = next(c for c in lb.columns if c.startswith("liability_"))
    central_cols = [c for c in lb.columns if "central" in c and c.endswith("_USD_M") and "p0" not in c and "p9" not in c]
    if central_cols:
        sort_col = central_cols[0]
    lb = lb.sort_values(sort_col, ascending=False).reset_index(drop=True)
    lb["rank"] = lb.index + 1
    return lb, pd.DataFrame(totals)
