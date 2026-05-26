"""EM-DAT disaster database loader and query helpers.

Data obtained under the EM-DAT Data Use Agreement (CRED/UCLouvain).
No redistribution. Cite as:
    EM-DAT: The Emergency Events Database — Université catholique de Louvain (UCL) — CRED,
    D. Guha-Sapir — www.emdat.be, Brussels, Belgium.
"""

from __future__ import annotations

import pandas as pd
from pathlib import Path

_PROC = Path(__file__).parents[2] / "data" / "processed"
_PARQUET = _PROC / "emdat_disasters.parquet"


def load_emdat() -> pd.DataFrame:
    """Load the processed EM-DAT parquet.

    Raises FileNotFoundError if the parquet has not been generated yet.
    Run notebooks/01-exploration/03_emdat_ingest.ipynb to create it.
    """
    if not _PARQUET.exists():
        raise FileNotFoundError(
            f"{_PARQUET} not found. "
            "Register at emdat.be, export a CSV, place it in data/raw/emdat/, "
            "then run notebooks/01-exploration/03_emdat_ingest.ipynb."
        )
    return pd.read_parquet(_PARQUET)


def search_events(
    country: str | None = None,
    year_start: int | None = None,
    year_end: int | None = None,
    disaster_type: str | None = None,
) -> pd.DataFrame:
    """Filter EM-DAT records.

    Parameters
    ----------
    country : ISO3 code, e.g. "AUS"
    year_start / year_end : inclusive year bounds on the event start year
    disaster_type : e.g. "Wildfire", "Flood", "Storm"

    Returns all matching rows as a DataFrame.
    """
    df = load_emdat()
    if country is not None:
        df = df[df["country_iso3"].str.upper() == country.upper()]
    if year_start is not None:
        df = df[df["start_year"] >= year_start]
    if year_end is not None:
        df = df[df["start_year"] <= year_end]
    if disaster_type is not None:
        df = df[df["disaster_type"].str.lower() == disaster_type.lower()]
    return df.reset_index(drop=True)


def get_event_damages(
    dis_no: str | None = None,
    **search_kwargs,
) -> dict:
    """Return a damage dict for a single matched EM-DAT event.

    Pass either a specific `dis_no` (e.g. "2019-0546-AUS") or keyword
    arguments accepted by `search_events` (country, year_start, year_end,
    disaster_type). Raises ValueError if zero or more than one event matches.

    Returns
    -------
    dict with keys:
        insured_usd      — insured losses in full USD (maps to conservative scenario)
        total_usd        — total economic damages in full USD (maps to central scenario)
        total_usd_2020   — CPI-adjusted to 2020 USD (if available, else equals total_usd)
        source           — "emdat"
        dis_no           — EM-DAT disaster ID
    """
    if dis_no is not None:
        df = load_emdat()
        matches = df[df["DisNo."] == dis_no]
    else:
        matches = search_events(**search_kwargs)

    if len(matches) == 0:
        raise ValueError(
            f"No EM-DAT records matched. "
            f"Query: dis_no={dis_no!r}, filters={search_kwargs}"
        )
    if len(matches) > 1:
        raise ValueError(
            f"{len(matches)} EM-DAT records matched — narrow the query or provide dis_no.\n"
            f"{matches[['DisNo.', 'event_name', 'start_year', 'country_iso3', 'disaster_type', 'total_damage_usd']].to_string()}"
        )

    row = matches.iloc[0]
    return {
        "insured_usd": float(row.get("insured_damage_usd", 0) or 0),
        "total_usd": float(row.get("total_damage_usd", 0) or 0),
        "total_usd_2020": float(row.get("total_damage_usd_2020", row.get("total_damage_usd", 0)) or 0),
        "source": "emdat",
        "dis_no": str(row["DisNo."]),
    }
