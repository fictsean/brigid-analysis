#!/usr/bin/env python3
"""Validate pipeline outputs against pinned literature & internal benchmarks.

Usage:
    python3 scripts/validate_pipeline.py

Exits non-zero if any *gating* benchmark fails, so it can guard a rebuild.
Benchmarks and their citations live in tests/validation_benchmarks.json.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from attribution.validation import (  # noqa: E402
    compute_metrics,
    load_benchmarks,
    evaluate,
    format_report,
    gating_failures,
)


def main() -> int:
    metrics = compute_metrics()
    results = evaluate(metrics, load_benchmarks())

    by_cat = {}
    for r in results:
        by_cat.setdefault(r["category"], []).append(r)

    print("=" * 78)
    print("ATTRIBUTION PIPELINE VALIDATION")
    print("=" * 78)
    for cat in ("literature", "internal", "golden"):
        rows = by_cat.get(cat)
        if not rows:
            continue
        print(f"\n[{cat.upper()}]")
        print(format_report(rows))

    n_pass = sum(r["status"] == "PASS" for r in results)
    n_fail = sum(r["status"] == "FAIL" for r in results)
    n_skip = sum(r["status"] == "SKIP" for r in results)
    fails = gating_failures(results)

    print("\n" + "-" * 78)
    print(f"PASS={n_pass}  FAIL={n_fail}  SKIP={n_skip}  (gating failures: {len(fails)})")
    if fails:
        print("\nGATING FAILURES:")
        for r in fails:
            print(f"  ✗ {r['metric']}: actual={r['actual']:.4g} not in "
                  f"[{r['range'][0]:g}, {r['range'][1]:g}]")
            print(f"      source: {r['source']}")
    print("=" * 78)
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
