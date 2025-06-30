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
SITUATIONS = [
    "Baseline",
    "Optimized",
]
OBJECTIVES = [
    "Summary",
    "Traffic",
    "Air quality",
    "Livability",
]
SEASONS = [
    "Summer",
    "Autumn",
    "Winter",
]
WEEKDAYS = [
    "Weekday",
    "Weekend",
]
MOBILITY_DEMAND = [
    "Low",
    "Regular",
    "High",
]
AREAS = [
    "Arabia",
    "Jätkäsaari",
    "Kamppi",
    "Vihdintie",
]
TIMELINE_OPTIONS = ["Average", "Sum"]
TIMELINE_FUNCTIONS = {"Average": "mean", "Sum": "sum"}
AQ_VARIABLES = [
    "Carbon monoxide",
    "Carbon dioxide",
    "Hydrocarbon",
    "Nitrogen oxides",
    "Respirable particles",
    "Fine particles",
]
TRAFFIC_VARIABLES = ["Mobility flow", "Speed", "Travel time", "Lost time", "Noise"]

# AQ index parameters
AQI_INDEX_THRESHOLDS = [0, 10, 25, 50, 75, np.inf]
AQ_INDEX_LABELS = ["good", "satisfactory", "fair", "poor", "very poor"]

# Hover layout for plots
HOVERS = dict(bgcolor="white", font_size=16)

# Global data variables
UNITS = {
    "Mobility flow": "# of passengers",
    "Speed": "m/s",
    "Travel time": "# of trips",
    "Lost time": "# of trips",
    "Noise": "dB",
    "Carbon monoxide": "mg",
    "Carbon dioxide": "mg",
    "Hydrocarbon": "mg",
    "Nitrogen oxides": "mg",
    "Respirable particles": "µg",
    "Fine particles": "µg",
}

# From variable-situation-to-dataset-columns mapping for filtering
# (Situation, variable) -> (dataset, [list of columns])
FROM_SITU_VAR_TO_DATA_COLS = {
    ("Baseline", "Trips"): (
        "Baseline trips",
        ["Travel time", "Lost time", "Mobility mode", "Mobility flow"],
    ),
    ("Baseline", "Mobility flow"): (
        "Baseline emissions",
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
    ("Baseline", "Speed"): (
        "Baseline emissions",
        [
            "Name",
            "Edge",
            "Simulation timestep",
            "Longitude",
            "Latitude",
            "Mobility flow",
            "Mobility mode",
            "Speed",
        ],
    ),
    ("Baseline", "Travel time"): (
        "Baseline trips",
        ["Mobility mode", "Travel time", "Mobility flow"],
    ),
    ("Baseline", "Lost time"): (
        "Baseline trips",
        ["Mobility mode", "Lost time", "Mobility flow"],
    ),
    ("Baseline", "Noise"): (
        "Baseline noise",
        [
            "Name",
            "Edge",
            "Simulation timestep",
            "Longitude",
            "Latitude",
            "Noise",
            "Mobility flow",
        ],
    ),
    ("Optimized", "Mobility flow"): (
        "Optimized emissions",
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
    ("Optimized", "Speed"): (
        "Optimized emissions",
        [
            "Name",
            "Edge",
            "Simulation timestep",
            "Longitude",
            "Latitude",
            "Mobility flow",
            "Mobility mode",
            "Speed",
        ],
    ),
    ("Optimized", "Travel time"): (
        "Optimized trips",
        ["Mobility mode", "Travel time", "Mobility flow"],
    ),
    ("Optimized", "Noise"): (
        "Optimized noise",
        [
            "Name",
            "Edge",
            "Simulation timestep",
            "Longitude",
            "Latitude",
            "Noise",
            "Mobility flow",
        ],
    ),
    ("Baseline", "Carbon monoxide"): (
        "Baseline emissions",
        [
            "Name",
            "Edge",
            "Simulation timestep",
            "Longitude",
            "Latitude",
            "Carbon monoxide",
            "Mobility mode",
            "Mobility flow",
        ],
    ),
    ("Baseline", "Carbon dioxide"): (
        "Baseline emissions",
        [
            "Name",
            "Edge",
            "Simulation timestep",
            "Longitude",
            "Latitude",
            "Carbon dioxide",
            "Mobility mode",
            "Mobility flow",
        ],
    ),
    ("Baseline", "Hydrocarbon"): (
        "Baseline emissions",
        [
            "Name",
            "Edge",
            "Simulation timestep",
            "Longitude",
            "Latitude",
            "Hydrocarbon",
            "Mobility mode",
            "Mobility flow",
        ],
    ),
    ("Baseline", "Nitrogen oxides"): (
        "Baseline emissions",
        [
            "Name",
            "Edge",
            "Simulation timestep",
            "Longitude",
            "Latitude",
            "Nitrogen oxides",
            "Mobility mode",
            "Mobility flow",
        ],
    ),
    ("Baseline", "Respirable particles"): (
        "Baseline emissions",
        [
            "Name",
            "Edge",
            "Simulation timestep",
            "Longitude",
            "Latitude",
            "Respirable particles",
            "Mobility mode",
            "Mobility flow",
        ],
    ),
    ("Baseline", "Fine particles"): (
        "Baseline emissions",
        [
            "Name",
            "Edge",
            "Simulation timestep",
            "Longitude",
            "Latitude",
            "Fine particles",
            "Mobility mode",
            "Mobility flow",
        ],
    ),
    ("Optimized", "Carbon monoxide"): (
        "Optimized emissions",
        [
            "Name",
            "Edge",
            "Simulation timestep",
            "Longitude",
            "Latitude",
            "Carbon monoxide",
            "Mobility mode",
            "Mobility flow",
        ],
    ),
    ("Optimized", "Carbon dioxide"): (
        "Optimized emissions",
        [
            "Name",
            "Edge",
            "Simulation timestep",
            "Longitude",
            "Latitude",
            "Carbon dioxide",
            "Mobility mode",
            "Mobility flow",
        ],
    ),
    ("Optimized", "Hydrocarbon"): (
        "Optimized emissions",
        [
            "Name",
            "Edge",
            "Simulation timestep",
            "Longitude",
            "Latitude",
            "Hydrocarbon",
            "Mobility mode",
            "Mobility flow",
        ],
    ),
    ("Optimized", "Nitrogen oxides"): (
        "Optimized emissions",
        [
            "Name",
            "Edge",
            "Simulation timestep",
            "Longitude",
            "Latitude",
            "Nitrogen oxides",
            "Mobility mode",
            "Mobility flow",
        ],
    ),
    ("Optimized", "Respirable particles"): (
        "Optimized emissions",
        [
            "Name",
            "Edge",
            "Simulation timestep",
            "Longitude",
            "Latitude",
            "Respirable particles",
            "Mobility mode",
            "Mobility flow",
        ],
    ),
    ("Optimized", "Fine particles"): (
        "Optimized emissions",
        [
            "Name",
            "Edge",
            "Simulation timestep",
            "Longitude",
            "Latitude",
            "Fine particles",
            "Mobility mode",
            "Mobility flow",
        ],
    ),
    ("Baseline", "Relocation rate"): (
        "Baseline livability",
        ["Name", "Longitude", "Latitude", "Relocation rate"],
    ),
    ("Optimized", "Relocation rate"): (
        "Optimized livability",
        ["Name", "Longitude", "Latitude", "Relocation rate"],
    ),
}
# Marks for optimization sliders
OPTIM_MARKS = {0: "Equal", 1: "First", 2: "Second"}

# Labels to variables, if updates are needed
LABELS = {"Vehicle": "Mobility flow"}
