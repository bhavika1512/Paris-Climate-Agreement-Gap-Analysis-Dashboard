"""
Configuration file for the CO2 Emissions Dashboard
"""

# Application settings
APP_TITLE = "Global CO2 Emissions Dashboard"
APP_ICON = "🌍"
APP_DESCRIPTION = "An interactive dashboard for exploring CO2 emissions data from the Global Carbon Budget 2022."

# Data paths
DATA_DIR = "data"

# Dataset paths - Using direct paths since files are already cleaned
TOTAL_EMISSIONS_FILE = f"{DATA_DIR}/GCB2022v27_MtCO2_flat.csv"
PER_CAPITA_EMISSIONS_FILE = f"{DATA_DIR}/GCB2022v27_percapita_flat.csv"
SOURCES_FILE = f"{DATA_DIR}/GCB2022v27_sources_flat.csv"

# Metadata files
TOTAL_EMISSIONS_METADATA = f"{DATA_DIR}/GCB2022v27_MtCO2_flat_metadata.json"
PER_CAPITA_METADATA = f"{DATA_DIR}/GCB2022v27_percapita_flat_metadata.json"

# Visualization settings
DEFAULT_CHART_HEIGHT = 500
DEFAULT_MAP_HEIGHT = 600

# Color schemes
EMISSION_SOURCES_COLORS = {
    "Coal": "#E57373",
    "Oil": "#FFB74D",
    "Gas": "#FFF176",
    "Cement": "#90CAF9",
    "Flaring": "#CE93D8",
    "Other": "#80CBC4"
}

CHOROPLETH_COLORSCALE = "Reds"
LINE_CHART_COLORSCALE = "viridis"

# Default values
DEFAULT_START_YEAR = 1990
DEFAULT_END_YEAR = 2021
TOP_N_COUNTRIES = 10

# Country groupings
REGIONS = {
    "North America": ["USA", "CAN", "MEX"],
    "Europe": ["DEU", "GBR", "FRA", "ITA", "ESP"],
    "Asia": ["CHN", "IND", "JPN", "KOR", "IDN"],
    "Middle East": ["SAU", "IRN", "ARE", "QAT", "KWT"],
    "Africa": ["ZAF", "NGA", "EGY", "DZA", "MAR"],
    "South America": ["BRA", "ARG", "COL", "CHL", "PER"],
    "Oceania": ["AUS", "NZL"]
}