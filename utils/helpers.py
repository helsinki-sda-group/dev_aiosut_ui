# utils/helpers.py
import numpy as np
import pandas as pd
import os
import glob
import plotly.express as px
import utils.constants as uc
import sys
import sumolib
import random
import xml.etree.ElementTree as ET
import gzip
import traci
import shutil

# Hover layout
hover_layout = dict(bgcolor="white", font_size=16)


def new_timeline(network, timestep_range):
    """
    Re-indexes timesteps from simulation seconds to minutes.
    """
    timesteps = np.arange(
        network["Simulation timestep"].min(),
        network["Simulation timestep"].max(),
        timestep_range * 60,
        dtype=int,
    )
    timestep_labels = timesteps // 60
    network["Timestep"] = pd.cut(
        network["Simulation timestep"],
        bins=timesteps,
        labels=timestep_labels[1:],
        right=False,
        include_lowest=True,
    )
    return network


def map_bounds(network):
    """
    Calculates the bounds for a heatmap.
    """
    west_bound = network["Longitude"].min()
    east_bound = network["Longitude"].max()
    south_bound = network["Latitude"].min()
    north_bound = network["Latitude"].max()
    map_bounds = {
        "west": west_bound * (1 - 2e-3),
        "east": east_bound * (1 + 2e-3),
        "south": south_bound * (1 - 5e-5),
        "north": north_bound * (1 + 5e-5),
    }
    return map_bounds


def spatial_scope(spatial_click_data, network):
    """
    Sets the location text and spatial scope for the data when the location is changed.
    """
    if spatial_click_data is None:
        location = "Location: Network"
    else:
        road_lon = spatial_click_data["points"][0]["lon"]
        road_lat = spatial_click_data["points"][0]["lat"]
        name = spatial_click_data["points"][0]["customdata"][0]
        location = f"Location: {name} ({road_lat:.2f} °N, {road_lon:.2f} °E)"
        edge = spatial_click_data["points"][0]["customdata"][1]
        network = network[network["Edge"] == edge]
    return network, location


def normalize_range(array, x, y):
    """
    Normalizes an array to a given range (x,y).
    """
    m = min(array)
    data_range = max(array) - m
    array = (array - m) / data_range
    range2 = y - x
    normalized = (array * range2) + x
    return list(normalized)


# Helper function to read data
def read_data(path):
    data = pd.read_csv(f"{path}", index_col=0)
    data = data.infer_objects()
    if "Mobility mode" in data.columns:
        data["Mobility mode"] = pd.Categorical(data["Mobility mode"], ordered=True)
    return data


# Datasets and column types
def get_data(
    area="kamppi",
    demand="regular",
    season="summer",
    time="weekday",
    situation="baseline",
    optimization=None,
    variable="Mobility flow",
):
    """
    Slices the required data from the dataset written on the disk.
    """
    dataset_name, dataset_cols = uc.FROM_VAR_TO_DATA_COLS[variable]
    if situation.lower() == "optimized":
        output_path = os.path.join(
            # ".",
            "simulation",
            "scenarios",
            f"{area.lower()}",
            f"{demand.lower()}_{season.lower()}_{time.lower()}",
            f"{situation.lower()}_{uc.OPTIMIZATION_SLIDER_VALUES[optimization]}",
            f"{dataset_name}.csv.gz",
        )
    else:
        output_path = os.path.join(
            # ".",
            "simulation",
            "scenarios",
            f"{area.lower()}",
            f"{demand.lower()}_{season.lower()}_{time.lower()}",
            f"{situation.lower()}",
            f"{dataset_name}.csv.gz",
        )
    dataset = read_data(output_path)[dataset_cols]
    # print(dataset.head())
    if "noise" in dataset_name:
        helper_dataset_name, _ = uc.FROM_SITU_VAR_TO_DATA_COLS[
            (situation, "Carbon dioxide")
        ]
        if situation == "optimized":
            helper_output_path = os.path.join(
                # ".",
                "simulation",
                "scenarios",
                f"{area.lower()}",
                f"{demand.lower()}_{season.lower()}_{time.lower()}",
                f"{situation.lower()}_{uc.OPTIMIZATION[optimization]}",
                f"{helper_dataset_name}.csv.gz",
            )
        else:
            helper_output_path = os.path.join(
                # ".",
                "simulation",
                "scenarios",
                f"{area.lower()}",
                f"{demand.lower()}_{season.lower()}_{time.lower()}",
                f"{situation.lower()}",
                f"{helper_dataset_name}.csv.gz",
            )
        helper_dataset = read_data(helper_output_path)
        helper_dataset = helper_dataset[
            ["Simulation timestep", "Edge", "Mobility flow"]
        ]
        helper_dataset = (
            helper_dataset.groupby(["Simulation timestep", "Edge"])
            .agg({"Mobility flow": "sum"})
            .reset_index()
        )
        dataset = dataset.merge(
            right=helper_dataset, on=["Simulation timestep", "Edge"]
        )
    return dataset


def create_heatmap(network, variable):
    """Creates an animated heatmap for with a capability to drilldown on a specific point."""
    legend_max = 1.2 * network[network[variable] != 0][variable].median()
    heatmap = px.density_map(
        data_frame=network,
        lat="Latitude",
        lon="Longitude",
        z=variable,
        radius=13,
        map_style="open-street-map",
        range_color=(0, legend_max),
        hover_data={
            "Name": True,
            "Edge": False,
            "Mobility flow": True,
            "Longitude": False,
            "Latitude": False,
            variable: True,
        },
        animation_frame="Timestep",
        title="Network heatmap",
    )
    # Customize the sliders with a larger font size and prefix
    sliders = [
        dict(
            currentvalue={"prefix": "Time (in minutes): "},
            font={"size": 14},
            pad={"t": 50},
        )
    ]
    # Update points' opacity on click
    heatmap.update_layout(
        clickmode="event+select",
        sliders=sliders,
        map_bounds=map_bounds(network=network),
        # labels=uc.LABELS,
    )
    # Sets the variable name and its unit as a legend to the color bar
    heatmap.layout["coloraxis"]["colorbar"][
        "title"
    ] = f"{variable} ({uc.UNITS[variable]})"
    return heatmap


def create_mobility_mode_avg_bar_plot(network, variable):
    """Creates a horizontal mobility mode -specific bar plot of averages."""
    bar_plot = px.bar(
        data_frame=network,
        x=variable,
        y="Mobility mode",
        color=variable,
        hover_data="Mobility flow",
        title=f"Average {variable.lower()} per mobility mode",
    )
    # Customize the hovers, title, axis labels and legend
    bar_plot.update_layout(
        hoverlabel=hover_layout,
        title_x=0.11,
        bargap=0.5,
        xaxis_title=f"Average {variable.lower()} ({uc.UNITS[variable]})",
        yaxis_title="Mobility mode",
        xaxis=dict(range=[0, network[variable].max() * 1.1]),
        # labels=uc.LABELS,
    )
    return bar_plot


def create_area_chart(network, variable):
    """Creates an area chart, where the x-axis is over time."""
    # Draw the area chart
    area_plot = px.area(
        data_frame=network,
        x="Timestep",
        y=variable,
        color="Mobility mode",
        color_discrete_sequence=px.colors.sequential.Plasma_r,
        title="Mobility mode time series",
    )
    # Customize the title and yaxis
    area_plot.update_layout(
        title_x=0.11,
        yaxis_title=f"{variable} ({uc.UNITS[variable]})",
        # labels=uc.LABELS,
    )
    # Output the plot
    return area_plot


def create_mobility_mode_histogram(network, variable):
    """Creates a mobility mode -specific histogram."""
    histogram = px.histogram(
        data_frame=network, x=variable, color="Mobility mode", barmode="overlay"
    )
    # Update the axis labels and the bars' gap
    histogram.update_layout(
        yaxis_title=uc.UNITS[variable],
        bargap=0.2,
        xaxis_title=f"{variable}",
        # labels=uc.LABELS,
    )
    # Output the plot
    return histogram


def _vehicle(
    type="fuel",
    accel=0.8,
    decel=4.5,
    sigma=0.5,
    length=5,
    maxSpeed=40,
    emissionClass="HBEFA4/PC_petrol_ltECE",
):
    return f"""\t<vType id="{type}" accel="{accel}" decel="{decel}" sigma="{sigma}" length="{length}" maxSpeed="{maxSpeed}" emissionClass="{emissionClass}"/>\n"""


def _trip(
    id,
    departureTime,
    origin,
    destination,
    type="fuel",
):
    return f"""\t<trip id="test_trip_{id}" type="{type}" depart="{departureTime}" from="{origin}" to="{destination}"/>\n"""


def _random_trips(
    f,
    net,
    cars=3000,
    trip_start=0,
    trip_end=3200,
    electrify=0.2,
):
    edges = net.getEdges()
    numberOfEdges = len(edges)
    f.write(_vehicle())
    if electrify > 0:
        f.write(_vehicle(type="electric", emissionClass="HBEFA4/PC_BEV"))
    departures = random.sample(range(trip_start, trip_end), cars)
    fuel = np.full(round(cars * (1.0 - electrify)), False, dtype=bool)
    electric = np.full(cars - len(fuel), True, dtype=bool)
    electric_generator = np.concatenate((fuel, electric))
    np.random.shuffle(electric_generator)
    departures = np.sort(departures)
    i = 0
    for departure in departures:
        path = None
        # Keep trying until there exists a path between the random origin and destination
        while path is None:
            originEdgeStruct = edges[random.randint(0, numberOfEdges - 1)]
            destinationEdgeStruct = edges[random.randint(0, numberOfEdges - 1)]
            path = net.getShortestPath(originEdgeStruct, destinationEdgeStruct)[0]
        originEdge = originEdgeStruct._id
        destinationEdge = destinationEdgeStruct._id
        strIndex = str(i)
        if electric_generator[i]:
            f.write(
                _trip(
                    id=strIndex,
                    departureTime=departure,
                    origin=originEdge,
                    destination=destinationEdge,
                    type="electric",
                )
            )
        else:
            f.write(
                _trip(
                    id=strIndex,
                    departureTime=departure,
                    origin=originEdge,
                    destination=destinationEdge,
                )
            )
        i += 1


def _write_route_file(
    net_file_path,
    rou_file_path,
    demand,
    season,
    day,
    seed,
):
    net = sumolib.net.readNet(net_file_path)
    random.seed(seed)
    np.random.seed(seed)

    with open(rou_file_path, "w") as f:
        f.write("""<?xml version="1.0" encoding="UTF-8"?>\n<routes>\n""")
        _random_trips(f=f, net=net, seed=seed, season=season, demand=demand, day=day)
        f.write("""</routes>""")


# Helper function to safely get attributes and convert types
def _get_attributes(element, attributes_map):
    """
    Extracts attributes from an XML element and converts them to specified types.

    Args:
        element (xml.etree.ElementTree.Element): The XML element to process.
        attributes_map (dict): A dictionary where keys are desired DataFrame column
                               names and values are tuples of (xml_attribute_name, type_constructor).

    Returns:
        dict: A dictionary of extracted and converted attribute values.
    """
    data = {}
    for col_name, (xml_attr, type_func) in attributes_map.items():
        value = element.get(xml_attr)
        if value is not None:
            try:
                data[col_name] = type_func(value)
            except (ValueError, TypeError):
                data[col_name] = None  # Handle conversion errors
        else:
            data[col_name] = None  # Attribute not present
    return data


# Convert net to csv
def _parse_net_xml(net_path):
    """
    Parses a SUMO network XML file (.net.xml) and extracts edge and lane information.

    Args:
        net_path (str): Path to the SUMO network XML file.

    Returns:
        pd.DataFrame: A DataFrame containing network edges, lanes, names, and coordinates.
    """
    net = sumolib.net.readNet(net_path)
    tree = ET.parse(net_path)
    root = tree.getroot()

    all_lanes_data = []

    for edge in root.iter("edge"):
        edge_type = edge.get("type")

        # Exclude internal edges
        if edge_type != "internal" and edge_type is not None:
            edge_id = edge.get("id")
            name = edge.get("name") if edge.get("name") is not None else "Unnamed road"
            shape_str = edge.get("shape")

            lon, lat = None, None
            if shape_str:
                points = shape_str.split()
                if (
                    len(points) >= 1
                ):  # Use the first point as a reasonable approximation if only one
                    # Use midpoint for better representation
                    center_point_str = points[len(points) // 2]
                    try:
                        x, y = map(float, center_point_str.split(","))
                        lon, lat = net.convertXY2LonLat(x, y)
                    except ValueError:
                        # Handle cases where point format is unexpected
                        pass

            for lane in edge.iter("lane"):
                lane_id = lane.get("id")
                all_lanes_data.append(
                    {
                        "Edge": edge_id,
                        "Name": name,
                        "Longitude": lon,
                        "Latitude": lat,
                        "Lane": lane_id,
                    }
                )

    net_df = pd.DataFrame(all_lanes_data)
    return net_df


# Aggregate the full xml output
def _parse_full_output_xml(file_path, net_df):
    """
    Parses a SUMO full output XML file and extracts vehicle and lane data.

    Args:
        file_path (str): Path to the SUMO full output XML file.
        net_df (pd.DataFrame): DataFrame from parse_net_xml containing lane info.

    Returns:
        tuple: A tuple containing two pandas DataFrames (lane_output_df, vehicle_output_df).
    """
    tree = ET.parse(file_path)
    root = tree.getroot()

    all_veh_data = []
    all_lane_data = []

    # Define attribute mappings for vehicles and lanes
    vehicle_attributes = {
        "Vehicle": ("id", str),
        "Mobility mode": ("type", str),
        "Carbon dioxide": ("CO2", float),
        "Carbon monoxide": ("CO", float),
        "Hydrocarbon": ("HC", float),
        "Nitrogen oxides": ("NOx", float),
        "Respirable particles": ("PMx", float),
        "Fuel": ("fuel", float),
        "Electricity": ("electricity", float),
        "Route": ("route", str),
        "Noise": ("noise", float),
        "Speed": ("speed", float),
    }

    lane_attributes = {
        "Lane": ("id", str),
        "Vehicles": ("vehicle_count", int),
        "Carbon dioxide": ("CO2", float),
        "Carbon monoxide": ("CO", float),
        "Hydrocarbon": ("HC", float),
        "Nitrogen oxides": ("NOx", float),
        "Respirable particles": ("PMx", float),
        "Noise": ("noise", float),
        "Average speed": ("meanspeed", float),
    }

    for data_point in root.iter("data"):
        timestep = float(data_point.get("timestep"))

        for vehicle in data_point.iter("vehicle"):
            veh_info = _get_attributes(vehicle, vehicle_attributes)
            veh_info["Simulation timestep"] = timestep
            veh_info["Mobility flow"] = 1  # Constant for vehicle count
            all_veh_data.append(veh_info)

        for edge in data_point.iter("edge"):
            edge_id = edge.get("id")
            edge_traveltime = float(edge.get("traveltime"))

            for lane in edge.iter("lane"):
                lane_info = _get_attributes(lane, lane_attributes)
                lane_info["Simulation timestep"] = timestep
                lane_info["Edge"] = edge_id
                lane_info["Edge travel time"] = edge_traveltime
                all_lane_data.append(lane_info)

    lane_output_df = pd.DataFrame(all_lane_data)
    vehicle_output_df = pd.DataFrame(all_veh_data)

    if not lane_output_df.empty:
        lane_output_df = lane_output_df.merge(net_df, on="Lane", how="left")

    return lane_output_df, vehicle_output_df


# Aggregate the lane noise output
def _parse_lane_noise_xml(file_path, net_df):
    """
    Parses a SUMO lane noise output XML file and extracts noise data per lane.

    Args:
        file_path (str): Path to the SUMO lane noise XML file.
        net_df (pd.DataFrame): DataFrame from parse_net_xml containing lane info.

    Returns:
        pd.DataFrame: A DataFrame containing lane noise data.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()

    all_noise_data = []
    noise_attributes = {
        "Lane": ("id", str),
        "Noise": ("noise", float),
    }

    for interval in root.iter("interval"):
        timestep = float(interval.get("end"))
        for lane in interval.iter("lane"):
            lane_noise_info = _get_attributes(lane, noise_attributes)
            lane_noise_info["Simulation timestep"] = timestep
            all_noise_data.append(lane_noise_info)

    results_df = pd.DataFrame(all_noise_data)
    if not results_df.empty:
        results_df = results_df.merge(net_df, on="Lane", how="left")
    return results_df


# Aggregate the edge noise output
def _parse_edge_noise_xml(file_path, net_df):
    """
    Parses a SUMO edge noise output XML file and extracts noise data per edge.

    Args:
        file_path (str): Path to the SUMO edge noise XML file.
        net_df (pd.DataFrame): DataFrame from parse_net_xml containing edge info.

    Returns:
        pd.DataFrame: A DataFrame containing edge noise data.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()

    all_noise_data = []
    noise_attributes = {
        "Edge": ("id", str),
        "Noise": ("noise", float),
    }

    for interval in root.iter("interval"):
        timestep = float(interval.get("end"))
        for edge in interval.iter("edge"):
            edge_noise_info = _get_attributes(edge, noise_attributes)
            edge_noise_info["Simulation timestep"] = timestep
            all_noise_data.append(edge_noise_info)

    results_df = pd.DataFrame(all_noise_data)
    if not results_df.empty:
        # Merge with a subset of net_df relevant for edges
        results_df = results_df.merge(
            net_df[["Edge", "Longitude", "Latitude", "Name"]].drop_duplicates(
                subset=["Edge"]
            ),
            on="Edge",
            how="left",
        )
    return results_df


# Aggregate the trip outputs
def _parse_trip_output_xml(file_path):
    """
    Parses a SUMO tripinfo output XML file and extracts trip data.

    Args:
        file_path (str): Path to the SUMO tripinfo XML file.

    Returns:
        pd.DataFrame: A DataFrame containing trip data.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()

    all_trip_data = []

    tripinfo_attributes = {
        "Trip": ("id", str),
        "Lost time": ("timeLoss", float),
        "Travel time": ("duration", float),
        "Mobility mode": ("vType", str),
    }

    emissions_attributes = {
        "Carbon dioxide": ("CO2_abs", float),
        "Carbon monoxide": ("CO_abs", float),
        "Hydrocarbon": ("HC_abs", float),
        "Nitrogen oxides": ("NOx_abs", float),
        "Respirable particles": ("PMx_abs", float),
        "Fuel": ("fuel", float),
        "Electricity": ("electricity", float),
    }

    for trip in root.iter("tripinfo"):
        trip_data = _get_attributes(trip, tripinfo_attributes)

        # Emissions are nested, so iterate and add to trip_data
        emissions_element = trip.find(
            "emissions"
        )  # Use find() as there's usually one emissions tag per tripinfo
        if emissions_element is not None:
            emissions_data = _get_attributes(emissions_element, emissions_attributes)
            trip_data.update(emissions_data)

        trip_data["Mobility flow"] = 1
        all_trip_data.append(trip_data)

    results_df = pd.DataFrame(all_trip_data)
    return results_df


# Aggregate the emission output
def _parse_emissions_xml(file_path, net_df):
    """
    Parses a SUMO emissions output XML file and extracts vehicle emission data.

    Args:
        file_path (str): Path to the SUMO emissions XML file.
        net_df (pd.DataFrame): DataFrame from parse_net_xml containing lane info.

    Returns:
        pd.DataFrame: A DataFrame containing vehicle emission data.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()

    all_emission_data = []

    vehicle_attributes = {
        "Vehicle": ("id", str),
        "Route": ("route", str),
        "Lane": ("lane", str),
        "Mobility mode": ("type", str),
        "Class": ("eclass", str),
        "Speed": ("speed", float),
        "Carbon dioxide": ("CO2", float),
        "Carbon monoxide": ("CO", float),
        "Hydrocarbon": ("HC", float),
        "Nitrogen oxides": ("NOx", float),
        "Respirable particles": ("PMx", float),
        "Fuel": ("fuel", float),
        "Electricity": ("electricity", float),
        "Noise": ("noise", float),
    }

    for timestep_element in root.iter("timestep"):
        timestep = float(timestep_element.get("time"))
        for vehicle in timestep_element.iter("vehicle"):
            veh_emission_info = _get_attributes(vehicle, vehicle_attributes)
            veh_emission_info["Simulation timestep"] = timestep
            veh_emission_info["Mobility flow"] = 1
            all_emission_data.append(veh_emission_info)

    results_df = pd.DataFrame(all_emission_data)
    if not results_df.empty:
        results_df = results_df.merge(net_df, on="Lane", how="left")
    return results_df


def _modify_config(
    scenario_folder, area_folder, config_folder, output_folder, net_file
):
    """
    Finds a configuration file, removes it and writes new one with specified values.

    Args:
        scenario_folder (str): the scenario folder path.
        area_folder (str): the area folder path.
        config_folder (str): the configuration file folder path.
        output_folder (str): the output folder path.
        net_file (str): the net file path.
    """
    additional_file_value = os.path.join(scenario_folder, "add.xml")
    net_file_value = os.path.join(net_file)
    route_file_value = os.path.join(area_folder, "rou.xml")
    tripinfo_file_value = os.path.join(output_folder, "trip_results.xml")
    emission_file_value = os.path.join(output_folder, "emission_results.xml")
    config_file = os.path.join(config_folder, "config.sumocfg")
    try:
        os.remove(config_file)
    except OSError:
        pass
    config_str = f"""<?xml version="1.0" encoding="UTF-8"?>
    <configuration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/sumoConfiguration.xsd">
        <input>
            <net-file value="{net_file_value}"/>
            <route-files value="{route_file_value}"/>
            <additional-files value="{additional_file_value}"/>
        </input>
        <output>
            <tripinfo-output value="{tripinfo_file_value}"/>
            <emission-output value="{emission_file_value}" excludeEmpty="false"/>
        </output>
    </configuration>"""
    with open(config_file, "w") as f:
        f.write(config_str)


def aggregate_outputs(
    net_path="simulation/scenarios/kamppi/baseline_net.xml",
    full_output_folder="simulation/scenarios/kamppi/regular_summer_weekday/optimized_equal",
):
    # Convert the output files of raw xml to gzipped csv
    net_df = _parse_net_xml(net_path)
    xml_output_files = glob.glob(f"{full_output_folder}/*.xml*")
    for filename in xml_output_files:
        file_without_extension = filename.split(".")[0]
        with open(filename, "rb") as f_in:
            with gzip.open(f"{filename}.gz", "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
                os.remove(f_in)
                # if "lane_noise" in f_out:
                #     lane_noise = parse_lane_noise_xml(f_out, net_df)
                #     lane_noise.to_csv(
                #         f"{file_without_extension}.csv.gz",
                #         compression="gzip",
                #     )
                if "edge_noise" in filename:
                    edge_noise = _parse_edge_noise_xml(f_out, net_df)
                    # print(edge_noise.head())
                    edge_noise.to_csv(
                        f"{file_without_extension}.csv.gz",
                        compression="gzip",
                    )
                elif "trip" in filename:
                    trip_info = _parse_trip_output_xml(f_out)
                    trip_info.to_csv(
                        f"{file_without_extension}.csv.gz",
                        compression="gzip",
                    )
                elif "emission" in filename:
                    emissions = _parse_emissions_xml(f_out, net_df)
                    emissions.to_csv(
                        f"{file_without_extension}.csv.gz",
                        compression="zip",
                    )
                os.remove(f_out)


# Simulate
def run_simulation(
    area="kamppi",
    season="summer",
    demand="regular",
    day="weekday",
    optimization="equal",
    seed=123,
):
    """
    Runs a SUMO simulation, zips the XML outputs and converts them into csv.

    Args:
        area (str): the area that is simulated.
        season (str): the season that is simulated.
        demand (str): the amount of mobility that is simulated.
        day (str): the time of week that is simulated, weekday or weekend.
        optimization (str): the optimization weights from the interface
    """
    for situation in ["baseline", "optimized"]:
        # Directory paths for outputs
        baseline_output_folder = os.path.join(
            ".",
            "simulation",
            "scenarios",
            str(area),
            f"{demand}_{season}_{day}_{situation}",
        )
        os.makedirs(baseline_output_folder, exist_ok=True)
        optim_output_folder = os.path.join(
            ".",
            "simulation",
            "scenarios",
            str(area),
            f"{demand}_{season}_{day}_{situation}_{optimization}",
        )
        os.makedirs(optim_output_folder, exist_ok=True)
        # If the outputs already exist, do not run the simulation loop
        if len(dir(optim_output_folder)) != 0 and len(dir(baseline_output_folder)) != 0:
            return
        # Run a new sim to create the outputs
        else:
            # Sanity check: sim will fail without SUMO_HOME
            if "SUMO_HOME" in os.environ:
                tools = os.path.join(os.environ["SUMO_HOME"], "tools")
                sys.path.append(tools)
            else:
                sys.exit("Please declare environment variable 'SUMO_HOME'")

            ## File paths
            # Where the baseline road network, routes and add.xml resides
            area_folder = os.path.join(".", "simulation", "scenarios", str(area))
            os.makedirs(area_folder, exist_ok=True)
            # Baseline net and additional file exist there
            baseline_net = os.path.join(area_folder, "baseline_net.xml")
            additional_file = os.path.join(config_folder, "add.xml")
            if not os.path.isfile(baseline_net) and not os.path.isfile(additional_file):
                raise KeyError(
                    f"The network file and additional file do not exist at: {area_folder}!"
                )
            # Where the .config should reside (only the latest version is preserved, as new one is written for each sim)
            config_folder = os.path.join(
                ".",
                "simulation",
            )
            os.makedirs(config_folder, exist_ok=True)
            # Where the optimized network and outputs should reside (specific for all scenarios, new ones written in each sim run)
            scenario_folder = os.path.join(
                ".",
                "simulation",
                str(area),
                str(demand),
                str(season),
                str(day),
                str(situation),
                str(optimization),
            )
            os.makedirs(scenario_folder, exist_ok=True)

            # Create OD matrix for a new simulation
            _write_route_file(
                rou_file_path=os.path.join(area_folder, "rou.xml"),
                net_file_path=baseline_net,
                demand=demand,
                season=season,
                day=day,
                seed=seed,
            )
            ## Start the correct loop: no optimization for baseline, RL for optimized
            # Fine-tune the add and config as needed
            _modify_config(
                scenario_folder=scenario_folder,
                area_folder=area_folder,
                config_folder=config_folder,
                output_folder=optim_output_folder,
                net_file=baseline_net,
            )
            config_file = os.path.join(config_folder, "config.sumocfg")
            traci.start(["sumo", "-c", config_file])
            # Let's go!
            while traci.simulation.getTime() < 3600:
                traci.simulationStep()
            sys.stdout.flush()
            traci.close()
            aggregate_outputs()
            # With RL loop: TODO
            # modify_config(
            #     scenario_folder=scenario_folder,
            #     area_folder=area_folder,
            #     config_folder=config_folder,
            #     output_folder=optim_output_folder,
            #     net_file=baseline_net
            # )
            return
