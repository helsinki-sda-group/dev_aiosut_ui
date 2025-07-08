# Imports
import numpy as np

# Interface text variables
MOBILITY_MODES = [
    "Pedestrians",
    "Private cars",
    "Bicycles",
    "Buses",
    "Trams",
]
OBJECTIVES = [
    "Summary",
    "Traffic",
    "Air quality",
    "Livability",
]
# Marks and values for optimization sliders
OPTIMIZATION_SLIDER_MARKS = {0: "Equal", 1: "First", 2: "Second"}
OPTIMIZATION_SLIDER_VALUES = {
    0: "equal",
    1: "traffic1",
    2: "traffic2",
}
TIMESTEPS = [
    {"label": "Minutes", "value": 1},
    {"label": "Quarters", "value": 15},
    {"label": "Half an hours", "value": 30},
    {"label": "Hours", "value": 60},
]
SITUATIONS = [
    {"label": "Baseline", "value": "baseline"},
    {"label": "Optimized", "value": "optimized"},
]
# Dropdowns
SEASONS = [
    {"label": "Spring (Feb-Apr)", "value": "spring", "disabled": True},
    {"label": "Summer (May-Aug)", "value": "summer", "disabled": True},
    {"label": "Autumn (Sept-Oct)", "value": "autumn"},
    {"label": "Winter (Nov-Jan)", "value": "winter", "disabled": True},
]
WEEKDAYS = [
    {"label": "Weekday", "value": "Weekday"},
    {"label": "Weekend", "value": "Weekend", "disabled": True},
]
MOBILITY_DEMAND = [
    {"label": "Low", "value": "low", "disabled": True},
    {"label": "Regular", "value": "regular"},
    {"label": "High", "value": "high", "disabled": True},
]
AREAS = [
    {"label": "Arabia", "value": "arabia", "disabled": True},
    {"label": "Jätkäsaari", "value": "high", "disabled": True},
    {"label": "Kamppi", "value": "kamppi"},
    {"label": "Vihdintie", "value": "vihdintie", "disabled": True},
]
TIMELINE_FUNCTIONS = [
    {"label": "Average", "value": "mean"},
    {"label": "Sum", "value": "sum"},
]
AQ_VARIABLES = [
    {"label": "Carbon monoxide", "value": "Carbon monoxide"},
    {"label": "Carbon dioxide", "value": "Carbon dioxide"},
    {"label": "Hydrocarbon", "value": "Hydrocarbon"},
    {"label": "Nitrogen oxides", "value": "Nitrogen oxides"},
    {"label": "Respirable particles", "value": "Respirable particles"},
    {"label": "Fine particles", "value": "Fine particles", "disabled": True},
]
TRAFFIC_VARIABLES = [
    {"label": "Mobility flow", "value": "Mobility flow"},
    {"label": "Speed", "value": "Speed"},
    {"label": "Travel time", "value": "Travel time"},
    {"label": "Lost time", "value": "Lost time"},
    {"label": "Noise", "value": "Noise"},
]

# AQ index parameters
AQI_INDEX_THRESHOLDS = [0, 10, 25, 50, 75, np.inf]
AQ_INDEX_LABELS = ["good", "satisfactory", "fair", "poor", "very poor"]

# Hover layout for plots
HOVERS = dict(bgcolor="white", font_size=16)

# Global data variables
UNITS = {
    "Mobility flow": "# of vehicles",
    "Vehicle": "# of vehicles",
    "Speed": "m/s",
    "Travel time": "in seconds",
    "Lost time": "in seconds",
    "Noise": "dB",
    "Carbon monoxide": "mg",
    "Carbon dioxide": "mg",
    "Hydrocarbon": "mg",
    "Nitrogen oxides": "mg",
    "Respirable particles": "µg",
    "Fine particles": "µg",
}

# From variable-situation-to-dataset-columns mapping for filtering
# Variable -> (dataset, [list of columns])
FROM_VAR_TO_DATA_COLS = {
    "Mobility flow": (
        "emission_results",
        [
            "Name",
            "Edge",
            "Simulation timestep",
            "Longitude",
            "Latitude",
            "Mobility flow",
            "Mobility mode",
            "Vehicle",
        ],
    ),
    "Speed": (
        "emission_results",
        [
            "Name",
            "Edge",
            "Simulation timestep",
            "Longitude",
            "Latitude",
            "Mobility flow",
            "Mobility mode",
            "Speed",
            "Vehicle",
        ],
    ),
    "Travel time": (
        "trip_results",
        ["Mobility mode", "Travel time", "Mobility flow"],
    ),
    "Lost time": (
        "trip_results",
        ["Mobility mode", "Lost time", "Mobility flow"],
    ),
    "Noise": (
        "edge_noise_results",
        [
            "Name",
            "Edge",
            "Simulation timestep",
            "Longitude",
            "Latitude",
            "Noise",
        ],
    ),
    "Noise2": (
        "emission_results",
        [
            "Name",
            "Edge",
            "Simulation timestep",
            "Longitude",
            "Latitude",
            "Noise",
            "Mobility flow",
            "Mobility mode",
            "Vehicle",
        ],
    ),
    "Carbon monoxide": (
        "emission_results",
        [
            "Name",
            "Edge",
            "Simulation timestep",
            "Longitude",
            "Latitude",
            "Carbon monoxide",
            "Mobility mode",
            "Mobility flow",
            "Vehicle",
        ],
    ),
    "Carbon dioxide": (
        "emission_results",
        [
            "Name",
            "Edge",
            "Simulation timestep",
            "Longitude",
            "Latitude",
            "Carbon dioxide",
            "Mobility mode",
            "Mobility flow",
            "Vehicle",
        ],
    ),
    "Hydrocarbon": (
        "emission_results",
        [
            "Name",
            "Edge",
            "Simulation timestep",
            "Longitude",
            "Latitude",
            "Hydrocarbon",
            "Mobility mode",
            "Mobility flow",
            "Vehicle",
        ],
    ),
    "Nitrogen oxides": (
        "emission_results",
        [
            "Name",
            "Edge",
            "Simulation timestep",
            "Longitude",
            "Latitude",
            "Nitrogen oxides",
            "Mobility mode",
            "Mobility flow",
            "Vehicle",
        ],
    ),
    "Respirable particles": (
        "emission_results",
        [
            "Name",
            "Edge",
            "Simulation timestep",
            "Longitude",
            "Latitude",
            "Respirable particles",
            "Mobility mode",
            "Mobility flow",
            "Vehicle",
        ],
    ),
    "Fine particles": (
        "emission_results",
        [
            "Name",
            "Edge",
            "Simulation timestep",
            "Longitude",
            "Latitude",
            "Fine particles",
            "Mobility mode",
            "Mobility flow",
            "Vehicle",
        ],
    ),
    "Relocation rate": (
        "Baseline livability",
        ["Name", "Longitude", "Latitude", "Relocation rate"],
    ),
}
# Labels to variables, if updates are needed
LABELS = {"Vehicle": "Mobility flow"}
