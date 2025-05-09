# %%
# Imports
import pandas as pd
import numpy as np
import sumolib
import xml.etree.ElementTree as et
from functools import reduce
import sys
import pyproj

# Helper function to calculate many vehicles' noise from a singular vehicle's noise
def noise_reduce(series):
    return reduce(
        lambda x, y: 10 * np.log10(np.power(10, x / 10) + np.power(10, y / 10)), series
    )

output = pd.read_csv("./kamppi/simulation_output/emissions_1.csv", sep=";")
net = sumolib.net.readNet("./kamppi/kamppi.net.xml")
teleports = pd.read_csv("./kamppi/simulation_output/teleports_1.csv")
# %%
edges = []
names = []
lons = []
lats = []
for edge in net.getEdges(withInternal=False):
    edge_id = edge.getID()
    name = edge.getName()
    points = edge.getShape()
    center = points[len(points)//2]
    lon, lat = net.convertXY2LonLat(center[0], center[1])
    edges.append(edge_id)
    names.append(name)
    lons.append(lon)
    lats.append(lat)
edge_df = pd.DataFrame(data={"Edge": edges, "Name": names, "Longitude": lons, "Latitude": lats})
# %%
lanes_to_edges = {}
unique_edges = list(edge_df["Edge"].dropna().unique())
unique_lanes = list(output["vehicle_lane"].dropna().unique())
for edge in unique_edges:
    lanes = list(filter(lambda unique_lanes: edge in unique_lanes, unique_lanes))
    for lane in lanes:
        lanes_to_edges[lane] = edge 
output = output.replace(lanes_to_edges)
output = pd.merge(output, edge_df, right_on="Edge", left_on="vehicle_lane")
unnecessary_columns = ["vehicle_waiting", "vehicle_pos", "vehicle_angle", "vehicle_eclass", "vehicle_id", "vehicle_route", "vehicle_x", "vehicle_y"]
output = output.drop(columns=unnecessary_columns)
bins = np.arange(0, 3660, 60, dtype=int)
labels = np.arange(0, 60, dtype=int)
output["timestep"] = pd.cut(output["timestep_time"], bins=bins, labels=labels)
output["Vehicles"] = np.ones(len(output), dtype=int)
output = (
    output.groupby(["timestep", "Edge", "vehicle_type"], observed=True)
    .agg(
        {
            "vehicle_noise": noise_reduce,
            "vehicle_CO": "sum",
            "vehicle_CO2": "sum",
            "vehicle_HC": "sum",
            "vehicle_NOx": "sum",
            "vehicle_PMx": "sum",
            "Vehicles": "sum",
            "Longitude": "first",
            "Latitude": "first",
            "Name": "first",
            "vehicle_fuel": "sum",
            "vehicle_electricity": "sum",
            "vehicle_speed": "mean",
        }
    )
    .reset_index()
)
output = output.dropna()
output = output.infer_objects()
output = output.rename(columns={"timestep": "Simulation timestep",
        "vehicle_type": "Mobility mode",
        "vehicle_noise": "Noise",
        "vehicle_CO2": "Carbon monoxide",
        "vehicle_CO": "Carbon dioxide",
        "vehicle_HC": "Hydrocarbon",
        "vehicle_NOx": "Nitrogen oxides",
        "vehicle_PMx": "Coarse particles",
        "vehicle_speed": "Average speed",
        "vehicle_fuel": "Fuel",
        "vehicle_electricity": "Electricity"})
# TODO: fill in the unobserved lanes
# num_unique_output_lanes = len(output_lanes)
# full_output = pd.DataFrame({"vehicle_lane": np.repeat(sorted(output_lanes), 60 * 2)})
# lanes = output[["vehicle_lane", "lon", "lat"]].drop_duplicates()
# full_output = full_output.merge(lanes, how="left")
# full_output["timestep"] = np.tile(
    # np.repeat(np.arange(0, 60, dtype=int), 2), num_unique_output_lanes
# )
# full_output["vehicle_type"] = np.tile(
    # ["electric", "fuel"], 60 * num_unique_output_lanes
# )
# full_output = full_output.merge(
    # output, how="left", on=["timestep", "vehicle_type", "vehicle_lane", "lon", "lat"]
# )
# full_output["timestep"] = full_output["timestep"].astype(str).astype(int) + 1
# numeric_cols = full_output.select_dtypes(include=["int", "float"]).columns
# full_output[numeric_cols] = full_output[numeric_cols].fillna(0)
# full_output.to_csv("tool/kamppi/simulation_output/clean_data.csv")
# %%
