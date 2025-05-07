# %%
# Imports
import pandas as pd
import numpy as np
import sumolib
import xml.etree.ElementTree as et
from difflib import SequenceMatcher as seq
from functools import reduce

# %%
output = pd.read_csv("/kamppi/simulation_output/emissions_1.csv", sep=";")
net = sumolib.net.readNet("/kamppi/kamppi.net.xml")
teleports = pd.read_csv("/kamppi/simulation_output/teleports_1.csv")

print(output.head())
# %%
lanes = pd.DataFrame(columns=["vehicle_lane", "lon", "lat"])
for edge in net.getEdges(withInternal=False):
    edge_id = edge.getID()
    raw_shape = edge.getShape()
    shape = edge.getRawShape()
    item = min(round(len(shape) / 2), 3)
    x, y = shape[item][0], shape[item][1]
    lon, lat = net.convertXY2LonLat(x, y)
    lanes.loc[len(lanes)] = [edge_id, lon, lat]
# %%
lane_to_edges = {}
unique_lanes = list(output["vehicle_lane"].unique())
unique_edges = list(lanes["vehicle_lane"].values)
for lane in unique_lanes:
    edge_ratios = []
    for edge in unique_edges:
        edge_ratios.append(seq(a=lane, b=edge).ratio())
    lane_to_edges[lane] = unique_edges[np.argmax(edge_ratios)]
output.replace({"vehicle_lane": lane_to_edges}, inplace=True)
output = pd.merge(output, lanes, on="vehicle_lane")
# %%
bins = np.arange(0, 3660, 60, dtype=int)
labels = np.arange(0, 60, dtype=int)
output["timestep"] = pd.cut(output["timestep_time"], bins=bins, labels=labels)
output["amount"] = np.ones(len(output), dtype=int)


# %%
# Helper function to calculate many vehicles' noise from a singular vehicle's noise
def noise_reduce(series):
    return reduce(
        lambda x, y: 10 * np.log10(np.power(10, x / 10) + np.power(10, y / 10)), series
    )


output_lanes = output["vehicle_lane"].unique()
output = (
    output.groupby(["timestep", "vehicle_lane", "vehicle_type"], observed=True)
    .agg(
        {
            "lon": "first",
            "lat": "first",
            "vehicle_noise": noise_reduce,
            "vehicle_CO": "sum",
            "vehicle_CO2": "sum",
            "vehicle_HC": "sum",
            "vehicle_NOx": "sum",
            "vehicle_PMx": "sum",
            "amount": "sum",
        }
    )
    .reset_index()
)
output.dropna(inplace=True)
num_unique_output_lanes = len(output_lanes)
full_output = pd.DataFrame({"vehicle_lane": np.repeat(sorted(output_lanes), 60 * 2)})
lanes = output[["vehicle_lane", "lon", "lat"]].drop_duplicates()
full_output = full_output.merge(lanes, how="left")
full_output["timestep"] = np.tile(
    np.repeat(np.arange(0, 60, dtype=int), 2), num_unique_output_lanes
)
full_output["vehicle_type"] = np.tile(
    ["electric", "fuel"], 60 * num_unique_output_lanes
)
full_output = full_output.merge(
    output, how="left", on=["timestep", "vehicle_type", "vehicle_lane", "lon", "lat"]
)
full_output.infer_objects()
full_output["timestep"] = full_output["timestep"].astype(str).astype(int)
numeric_cols = full_output.select_dtypes(include=["int", "float"]).columns
full_output[numeric_cols] = full_output[numeric_cols].fillna(0)
full_output = full_output.rename(
    {
        "vehicle_lane": "Road",
        "lon": "Longitude",
        "lat": "Latitude",
        "timestep": "Simulation timestep",
        "vehicle_type": "Mobility mode",
        "vehicle_noise": "Noise",
        "vehicle_CO2": "Carbon monoxide",
        "vehicle_CO": "Carbon dioxide",
        "vehicle_HC": "Hydrocarbon",
        "vehicle_NOx": "Nitrogen oxides",
        "vehicle_PMx": "Coarse particles",
        "amount": "Vehicles",
    }
)
full_output.to_csv("tool/kamppi/simulation_output/clean_data.csv")
