"""Shared constants for the attribution pipeline."""

# Annual average AUD→USD exchange rates (RBA), keyed by event year.
# Single source of truth — do not hardcode FX rates in notebooks.
AUD_TO_USD = {
    2020: 0.69,  # Black Summer 2019–20 damages are quoted in 2020 AUD
    2022: 0.70,  # 2022 SE QLD floods
}

# Clausius-Clapeyron scaling rates for precipitation extremes (fraction per °C)
CC_RATE_STANDARD = 0.07  # thermodynamic surface C-C rate
CC_RATE_HIGH = 0.14      # dynamic amplification upper sensitivity

# Climatology baseline used across all events
CLIM_START, CLIM_END = 1961, 1990

# GEV shape parameter bounds (ξ, WWA convention). scipy's genextreme uses c = -ξ.
GEV_SHAPE_BOUNDS = (-0.4, 0.4)
