"""Validation harness for the attribution pipeline.

Pins the key pipeline outputs against (a) published-literature anchors and
(b) internal-consistency / conservation invariants, so that methodological
drift — like the LEI-dropna bug (2026-06-17) or the fossil-CO2-denominator
over-attribution (2026-06-24) — is caught automatically rather than discovered
by accident.

Benchmarks live in ``tests/validation_benchmarks.json`` (one source of truth,
each with a citation/DOI). ``compute_metrics`` derives the actual values from
the git-tracked ``data/processed`` outputs; ``evaluate`` compares them.

No third-party test framework is required (pytest is not a project dependency) —
``scripts/validate_pipeline.py`` is a plain CLI runner.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
PROC = REPO_ROOT / "data" / "processed"
BENCHMARKS = REPO_ROOT / "tests" / "validation_benchmarks.json"

ARAMCO = "Saudi Aramco"
ANALYSIS_YEAR = 2020


def compute_metrics(proc: Path = PROC) -> dict:
    """Derive all benchmarked metrics from the processed pipeline outputs.

    Missing inputs yield a ``None`` metric (reported as SKIP) rather than an
    exception, so the harness degrades gracefully on a partial checkout.
    """
    m: dict[str, float | None] = {}

    def _read(name, reader):
        try:
            return reader(proc / name)
        except Exception:
            return None

    w = _read("entity_warming_contribution.parquet", pd.read_parquet)
    fair = _read("fair_global_temperature.parquet", pd.read_parquet)
    cm = _read("cm_entity_year.parquet", pd.read_parquet)
    bs_pr = _read("black_summer_pr_era5.csv", pd.read_csv)
    qld_pr = _read("qld_floods_pr_era5.csv", pd.read_csv)
    bs_tot = _read("black_summer_scenario_totals.csv", pd.read_csv)
    qld_tot = _read("qld_floods_scenario_totals.csv", pd.read_csv)

    fair_2020 = None
    if fair is not None:
        f = fair.set_index("year")["t_p50"]
        fair_2020 = float(f.loc[ANALYSIS_YEAR])
        m["fair_warming_2011_2020_degC"] = float(f.loc[2011:2020].mean())

    if w is not None:
        m["n_entities"] = int(len(w))
        m["collective_share"] = float(w["global_share"].sum())
        m["collective_warming_degC"] = float(w["warming_p50_degC"].sum())
        if fair_2020:
            m["collective_warming_fraction"] = m["collective_warming_degC"] / fair_2020
            # Coherence: warming_p50 must equal global_share * total ΔT for every entity.
            resid = (w["warming_p50_degC"] - w["global_share"] * fair_2020).abs()
            m["share_warming_coherence_max_abs"] = float(resid.max())
        ar = w[w["parent_entity"].str.contains(ARAMCO, na=False)]
        if len(ar):
            m["aramco_warming_degC"] = float(ar["warming_p50_degC"].iloc[0])

    if cm is not None:
        m["cm_total_2024_GtCO2e"] = float(cm[cm.year <= 2024]["total_emissions_MtCO2e"].sum() / 1000)
        m["cm_total_2022_GtCO2e"] = float(cm[cm.year <= 2022]["total_emissions_MtCO2e"].sum() / 1000)

    if bs_pr is not None:
        m["blacksummer_pr"] = float(bs_pr.iloc[0]["pr"])
        m["blacksummer_far"] = float(bs_pr.iloc[0]["far"])
    if qld_pr is not None:
        m["qld_pr"] = float(qld_pr.iloc[0]["pr"])
        m["qld_far"] = float(qld_pr.iloc[0]["far"])

    if bs_tot is not None:
        row = bs_tot[bs_tot["scenario"] == "central"].iloc[0]
        identity = row["cm_coverage_share"] * row["far"] * row["damages_usd_b"]
        m["blacksummer_liability_reproduces_resid_usd_b"] = abs(
            float(row["total_attributed_usd_b"]) - float(identity)
        )
        m["blacksummer_central_usd_b"] = float(row["total_attributed_usd_b"])
    if qld_tot is not None:
        m["qld_central_usd_b"] = float(
            qld_tot[qld_tot["scenario"] == "central"].iloc[0]["total_attributed_usd_b"]
        )

    return m


def load_benchmarks(path: Path = BENCHMARKS) -> list[dict]:
    data = json.loads(Path(path).read_text())
    return data["benchmarks"]


def evaluate(metrics: dict, benchmarks: list[dict]) -> list[dict]:
    """Return one result row per benchmark: status PASS / FAIL / SKIP."""
    results = []
    for b in benchmarks:
        name = b["metric"]
        lo, hi = b["range"]
        actual = metrics.get(name)
        if actual is None:
            status = "SKIP"
        elif lo <= actual <= hi:
            status = "PASS"
        else:
            status = "FAIL"
        results.append(
            {
                "metric": name,
                "status": status,
                "actual": actual,
                "range": [lo, hi],
                "unit": b.get("unit", ""),
                "category": b.get("category", ""),
                "gating": bool(b.get("gating", False)),
                "source": b.get("source", ""),
            }
        )
    return results


def format_report(results: list[dict]) -> str:
    lines = []
    width = max((len(r["metric"]) for r in results), default=10)
    for r in results:
        actual = r["actual"]
        a = f"{actual:.4g}" if isinstance(actual, (int, float)) else "—"
        rng = f"[{r['range'][0]:g}, {r['range'][1]:g}]"
        gate = "gating" if r["gating"] else "info"
        flag = {"PASS": "✓", "FAIL": "✗", "SKIP": "·"}[r["status"]]
        lines.append(
            f"  {flag} {r['status']:4s} {r['metric']:<{width}s}  actual={a:>10s}  "
            f"expected={rng:>16s}  {r['unit']:<8s} [{r['category']}/{gate}]"
        )
    return "\n".join(lines)


def gating_failures(results: list[dict]) -> list[dict]:
    return [r for r in results if r["gating"] and r["status"] == "FAIL"]
