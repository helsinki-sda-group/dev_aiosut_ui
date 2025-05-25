import sys
import sumolib
import random
import time
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import os
import gzip
import tqdm
import traci
import shutil
import glob


def vehicle(
    type="fuel",
    accel=0.8,
    decel=4.5,
    sigma=0.5,
    length=5,
    maxSpeed=40,
    emissionClass="HBEFA4/PC_petrol_ltECE",
):
    return f"""\t<vType id="{type}" accel="{accel}" decel="{decel}" sigma="{sigma}" length="{length}" maxSpeed="{maxSpeed}" emissionClass="{emissionClass}"/>\n"""


def trip(
    id,
    departureTime,
    origin,
    destination,
    type="fuel",
):
    return f"""\t<trip id="test_trip_{id}" type="{type}" depart="{departureTime}" from="{origin}" to="{destination}"/>\n"""


def randomTrip(
    f,
    cars,
    net,
    trip_start,
    trip_end,
    electrify,
    seed,
):
    random.seed(seed)
    np.random.seed(seed)
    edges = net.getEdges()
    numberOfEdges = len(edges)
    f.write(vehicle())
    if electrify > 0:
        f.write(vehicle(type="electric", emissionClass="HBEFA4/PC_BEV"))
    departures = random.sample(range(trip_start, trip_end), cars)
    not_electric = np.full(round(cars * (1.0 - electrify)), False, dtype=bool)
    electric = np.full(cars - len(not_electric), True, dtype=bool)
    electric = np.random.shuffle(np.concatenate((not_electric, electric)))
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
        if electric:
            f.write(
                trip(
                    id=strIndex,
                    departureTime=departure,
                    origin=originEdge,
                    destination=destinationEdge,
                    type="electric",
                )
            )
        else:
            f.write(
                trip(
                    id=strIndex,
                    departureTime=departure,
                    origin=originEdge,
                    destination=destinationEdge,
                )
            )
        i += 1


def writeRoutes(
    cars,
    trip_start,
    trip_end,
    electrify,
    seed,
    net_file_path,
    rou_file_path,
):
    net = sumolib.net.readNet(net_file_path)

    with open(rou_file_path, "w") as f:
        f.write("""<?xml version="1.0" encoding="UTF-8"?>\n<routes>\n""")
        randomTrip(
            f,
            cars,
            net,
            trip_start=trip_start,
            trip_end=trip_end,
            electrify=electrify,
            seed=seed,
        )
        f.write("""</routes>""")


# Aggregate the net
def net_output(net_path):
    net = sumolib.net.readNet(net_path)
    tree = ET.parse(net_path)
    edges = []
    names = []
    lanes = []
    lons = []
    lats = []
    file = tree.getroot()
    for edge in file.iter("edge"):
        edge_type = edge.get("type")

        # Exclude internal edges
        if edge_type != "internal" and edge_type is not None:

            # Iterate edges
            edge_id = edge.get("id")
            name = edge.get("name")
            if name is None:
                name = "Unnamed road"
            shape = edge.get("shape")
            if shape is not None:
                points = shape.split()
                if len(points) >= 2:
                    center = points[len(points) // 2]
                    split = center.split(",")
                    lon, lat = net.convertXY2LonLat(float(split[0]), float(split[1]))

            # Iterate lanes for an edge
            for lane in edge.iter("lane"):
                lane_id = lane.get("id")
                edges.append(edge_id)
                names.append(name)
                lanes.append(lane_id)
                lons.append(lon)
                lats.append(lat)

    net_df = pd.DataFrame(
        data={
            "Edge": edges,
            "Name": names,
            "Longitude": lons,
            "Latitude": lats,
            "Lane": lanes,
        }
    )
    return net_df


# Aggregate the full output
def full_output(file, net_df):
    # Vehicle lists
    veh_times = []
    veh_types = []
    veh_ids = []
    veh_co2s = []
    veh_cos = []
    veh_hcs = []
    veh_noxs = []
    veh_pmxs = []
    veh_fuels = []
    veh_elecs = []
    veh_routes = []
    veh_noises = []
    veh_speeds = []

    # Road lists
    lane_times = []
    edge_traveltimes = []
    edge_ids = []
    lane_vehicles = []
    lane_ids = []
    lane_co2s = []
    lane_cos = []
    lane_hcs = []
    lane_noxs = []
    lane_pmxs = []
    lane_noises = []
    lane_speeds = []

    tree = ET.parse(file)
    root = tree.getroot()

    for data_point in root.iter("data"):
        timestep = data_point.get("timestep")
        for vehicle in data_point.iter("vehicle"):
            veh_times.append(timestep)
            veh_ids.append(vehicle.get("id"))
            veh_types.append(vehicle.get("type"))
            veh_co2s.append(vehicle.get("CO2"))
            veh_cos.append(vehicle.get("CO"))
            veh_hcs.append(vehicle.get("HC"))
            veh_noxs.append(vehicle.get("NOx"))
            veh_pmxs.append(vehicle.get("PMx"))
            veh_fuels.append(vehicle.get("fuel"))
            veh_elecs.append(vehicle.get("electricity"))
            veh_noises.append(vehicle.get("noise"))
            veh_routes.append(vehicle.get("route"))
            veh_speeds.append(vehicle.get("speed"))
        for edge in data_point.iter("edge"):
            edge_traveltime = edge.get("traveltime")
            edge_id = edge.get("id")
            for lane in edge.iter("lane"):
                lane_times.append(timestep)
                edge_ids.append(edge_id)
                edge_traveltimes.append(edge_traveltime)
                lane_ids.append(lane.get("id"))
                lane_vehicles.append(lane.get("vehicle_count"))
                lane_co2s.append(lane.get("CO2"))
                lane_cos.append(lane.get("CO"))
                lane_hcs.append(lane.get("HC"))
                lane_noxs.append(lane.get("NOx"))
                lane_pmxs.append(lane.get("PMx"))
                lane_noises.append(lane.get("noise"))
                lane_speeds.append(lane.get("meanspeed"))

    lane_output = pd.DataFrame(
        data={
            "Simulation timestep": lane_times,
            "Lane": lane_ids,
            "Edge": edge_ids,
            "Edge travel time": edge_traveltimes,
            "Noise": veh_noises,
            "Carbon dioxide": veh_co2s,
            "Carbon monoxide": veh_cos,
            "Hydrocarbon": veh_hcs,
            "Nitrogen oxides": veh_noxs,
            "Coarse particles": veh_pmxs,
            "Vehicles": lane_vehicles,
            "Average speed": lane_speeds,
        }
    )
    lane_output = lane_output.merge(net_df, on="Lane")

    vehicle_output = pd.DataFrame(
        data={
            "Simulation timestep": veh_times,
            "Vehicle": veh_ids,
            "Route": veh_routes,
            "Mobility mode": veh_types,
            "Speed": veh_speeds,
            "Carbon dioxide": veh_co2s,
            "Carbon monoxide": veh_cos,
            "Hydrocarbon": veh_hcs,
            "Nitrogen oxides": veh_noxs,
            "Coarse particles": veh_pmxs,
            "Noise": veh_noises,
            "Fuel": veh_fuels,
            "Electricity": veh_elecs,
        }
    )
    return lane_output, vehicle_output


# Aggregate the lane noise output
def lane_noise_output(file, net_df):
    tree = ET.parse(file)
    root = tree.getroot()

    timesteps = []
    lane_ids = []
    noises = []

    for data_point in root.iter("interval"):
        timestep = data_point.get("end")
        for lane in data_point.iter("lane"):
            lane_id = lane.get("id")
            noise = lane.get("noise")
            timesteps.append(timestep)
            lane_ids.append(lane_id)
            noises.append(noise)

    results = pd.DataFrame(
        data={
            "Lane": lane_ids,
            "Simulation timestep": timesteps,
            "Noise": noises,
        }
    )
    results = results.merge(net_df, on="Lane")
    return results


# Aggregate the edge noise output
def edge_noise_output(file, net_df):
    tree = ET.parse(file)
    root = tree.getroot()

    timesteps = []
    edge_ids = []
    noises = []

    for data_point in root.iter("interval"):
        timestep = data_point.get("end")
        for edge in data_point.iter("edge"):
            edge_id = edge.get("id")
            noise = edge.get("noise")
            timesteps.append(timestep)
            edge_ids.append(edge_id)
            noises.append(noise)

    results = pd.DataFrame(
        data={
            "Edge": edge_ids,
            "Simulation timestep": timesteps,
            "Noise": noises,
        }
    )
    results = results.merge(
        net_df[["Edge", "Longitude", "Latitude", "Name"]], on="Edge"
    )
    return results


# Aggregate the trip outputs
def trip_output(file):
    tree = ET.parse(file)
    root = tree.getroot()

    trip_ids = []
    trip_traveltimes = []
    trip_types = []
    trip_losses = []
    trip_co2s = []
    trip_cos = []
    trip_hcs = []
    trip_noxs = []
    trip_pmxs = []
    trip_fuels = []
    trip_elecs = []

    for trip in root.iter("tripinfo"):
        id = trip.get("id")
        timeloss = trip.get("timeLoss")
        traveltime = trip.get("duration")
        type = trip.get("vType")
        for emissions in trip.iter("emissions"):
            trip_ids.append(id)
            trip_losses.append(timeloss)
            trip_traveltimes.append(traveltime)
            trip_types.append(type)
            trip_co2s.append(emissions.get("CO2_abs"))
            trip_cos.append(emissions.get("CO_abs"))
            trip_hcs.append(emissions.get("HC_abs"))
            trip_noxs.append(emissions.get("NOx_abs"))
            trip_pmxs.append(emissions.get("PMx_abs"))
            trip_fuels.append(emissions.get("fuel"))
            trip_elecs.append(emissions.get("electricity"))

    results = pd.DataFrame(
        data={
            "Trip": trip_ids,
            "Travel time": trip_traveltimes,
            "Lost time": trip_losses,
            "Mobility mode": trip_types,
            "Carbon dioxide": trip_co2s,
            "Carbon monoxide": trip_cos,
            "Hydrocarbon": trip_hcs,
            "Nitrogen oxides": trip_noxs,
            "Coarse particles": trip_pmxs,
        }
    )
    return results


# Aggregate the emission output
def emissions_output(file, net_df):
    tree = ET.parse(file)
    root = tree.getroot()

    veh_ids = []
    veh_routes = []
    veh_lanes = []
    veh_types = []
    veh_classes = []
    veh_speeds = []
    veh_times = []
    veh_co2s = []
    veh_cos = []
    veh_hcs = []
    veh_noxs = []
    veh_pmxs = []
    veh_fuels = []
    veh_elecs = []
    veh_noises = []

    for time in root.iter("timestep"):
        timestep = time.get("time")
        for vehicle in time.iter("vehicle"):
            lane = vehicle.get("lane")
            veh_ids.append(vehicle.get("id"))
            veh_routes.append(vehicle.get("route"))
            veh_lanes.append(lane)
            veh_types.append(vehicle.get("type"))
            veh_classes.append(vehicle.get("eclass"))
            veh_speeds.append(vehicle.get("speed"))
            veh_times.append(timestep)
            veh_co2s.append(vehicle.get("CO2"))
            veh_cos.append(vehicle.get("CO"))
            veh_hcs.append(vehicle.get("HC"))
            veh_noxs.append(vehicle.get("NOx"))
            veh_pmxs.append(vehicle.get("PMx"))
            veh_fuels.append(vehicle.get("fuel"))
            veh_elecs.append(vehicle.get("electricity"))
            veh_noises.append(vehicle.get("noise"))

    results = pd.DataFrame(
        data={
            "Vehicle": veh_ids,
            "Route": veh_routes,
            "Lane": veh_lanes,
            "Mobility mode": veh_types,
            "Class": veh_classes,
            "Speed": veh_speeds,
            "Simulation timestep": veh_times,
            "Carbon dioxide": veh_co2s,
            "Carbon monoxide": veh_cos,
            "Hydrocarbon": veh_hcs,
            "Nitrogen oxides": veh_noxs,
            "Coarse particles": veh_pmxs,
            "Fuel": veh_fuels,
            "Electricity": veh_elecs,
            "Noise": veh_noises,
        }
    )
    results = results.merge(net_df, on="Lane")
    return results


# Read the simulation outputs and aggregate them
def aggregateOutputs(
    area="kamppi",
):
    # output_folder = f"./tool/{area}/output"
    output_path = os.path.join(".", "simulation", str(area), "output")
    # net_path = f"./tool/{area}/net.xml"
    net_path = os.path.join(".", "simulation", str(area), "input", "net.xml")
    print("Converting outputs...")
    net_df = net_output(net_path)
    for file in tqdm.tqdm(os.listdir(output_path)):
        if file.endswith(".gz"):
            file_without_extension = file.split(".")[0]
            full_path = os.path.join(output_path, file)
            print(full_path)
            gzip_file = gzip.open(full_path, "rb")
            export = os.path.join(output_path, file_without_extension)
            if "lane_noise" in file:
                lane_noise = lane_noise_output(gzip_file, net_df)
                lane_noise.to_csv(f"{export}.csv")
            elif "edge_noise" in file:
                edge_noise = edge_noise_output(gzip_file, net_df)
                edge_noise.to_csv(f"{export}.csv")
            elif "trip" in file:
                trip_info = trip_output(gzip_file)
                trip_info.to_csv(f"{export}.csv")
            elif "emission" in file:
                emissions = emissions_output(gzip_file, net_df)
                emissions.to_csv(f"{export}.csv")
    print("Done!")


def runSimulation(
    cars=3000,
    simulation_end=3600,
    area="kamppi",
    trip_start=0,
    trip_end=3500,
    electrify=0.2,
    seed=123,
):
    # Sanity check
    if "SUMO_HOME" in os.environ:
        tools = os.path.join(os.environ["SUMO_HOME"], "tools")
        sys.path.append(tools)
    else:
        sys.exit("Please declare environment variable 'SUMO_HOME'")

    # Create directories for outputs and configurations
    full_input_folder = os.path.join(".", "simulation", str(area), "input")
    full_output_folder = os.path.join(".", "simulation", str(area), "output")
    shutil.rmtree(full_output_folder)
    os.makedirs(full_input_folder, exist_ok=True)
    os.makedirs(full_output_folder, exist_ok=True)
    # old_output_files = glob.glob(output_folder)
    # for file in old_output_files:
    # os.remove(file)

    # Create routes
    writeRoutes(
        rou_file_path=os.path.join(full_input_folder, "rou.xml"),
        net_file_path=os.path.join(full_input_folder, "net.xml"),
        cars=cars,
        trip_start=trip_start,
        trip_end=trip_end,
        electrify=electrify,
        seed=seed,
    )

    # Create other configuration files
    additional_file_write = os.path.join(".", "simulation", str(area), "additional.xml")
    additional_file_value = os.path.join("additional.xml")
    net_file = os.path.join("input", "net.xml")
    route_file = os.path.join("input", "rou.xml")
    config_file_write = os.path.join(".", "simulation", str(area), "config.sumocfg")
    tripinfo_file_value = os.path.join("output", "trip_results.xml")
    emission_file_value = os.path.join("output", "emission_results.xml")
    edge_noise_file_value = os.path.join("output", "edge_noise_results.xml")
    # lane_noise_file_value = os.path.join("output", "lane_noise_results.xml")

    # Additional file
    additional_root = ET.Element("additional")
    ET.SubElement(
        additional_root,
        "edgeData",
        file=edge_noise_file_value,
        period="1",
        type="harmonoise",
        id="edge-noise",
    )
    # ET.SubElement(
    #     additional_root,
    #     "laneData",
    #     file=lane_noise_file,
    #     period="1",
    #     type="harmonoise",
    #     id="lane-noise",
    # )
    additional_tree = ET.ElementTree(additional_root)
    additional_tree.write(additional_file_write)

    # Configuration file
    config_root = ET.Element("configuration")
    config_root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    config_root.set(
        "xsi:noNamespaceSchemaLocation",
        "http://sumo.dlr.de/xsd/sumoConfiguration.xsd",
    )
    config_input = ET.SubElement(config_root, "input")
    ET.SubElement(config_input, "net-file", value=net_file)
    ET.SubElement(config_input, "route-files", value=route_file)
    ET.SubElement(config_input, "additional-files", value=additional_file_value)
    config_output = ET.SubElement(config_root, "output")
    ET.SubElement(config_output, "output-prefix", value="TIME_")
    ET.SubElement(
        config_output,
        "tripinfo-output",
        value=tripinfo_file_value,
    )
    ET.SubElement(config_output, "emission-output", value=emission_file_value)
    config_tree = ET.ElementTree(config_root)
    config_tree.write(config_file_write)

    # Start the simulation with the above configuration files
    config_file_read = os.path.join(".", "simulation", str(area), "config.sumocfg")
    traci.start(["sumo", "-c", config_file_read])

    while traci.simulation.getTime() < simulation_end:
        traci.simulationStep()
    sys.stdout.flush()
    traci.close()

    # Zip the output files
    xml_output_files = glob.glob(f"{full_output_folder}/*.xml*")
    for filename in xml_output_files:
        with open(filename, "rb") as f_in:
            with gzip.open(f"{filename}.gz", "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove(filename)
    return


# Helper function to read data
def read_sumo_data(path):
    data = pd.read_csv(f"{path}", index_col=0)
    if "emission" in path or "trip" in path:
        data["Amount"] = 1
    data = data.infer_objects()
    if "Mobility mode" in data.columns:
        data["Mobility mode"] = pd.Categorical(data["Mobility mode"], ordered=True)
    return data


# Datasets and column types
def readData(area="kamppi"):
    output_path = os.path.join("simulation", str(area), "output")
    datasets = {}
    for file in glob.glob(f"{output_path}/*.csv"):
        if "emission" in file:
            datasets["Current emissions"] = read_sumo_data(file)
            datasets["Optimized emissions"] = read_sumo_data(file)
        # elif "lane_noise" in file:
        #     datasets["Current lane noise"] = read_sumo_data(file)
        #     datasets["Optimized lane noise"] = read_sumo_data(file)
        elif "edge_noise" in file:
            datasets["Current edge noise"] = read_sumo_data(file)
            datasets["Optimized edge noise"] = read_sumo_data(file)
        elif "trip" in file:
            datasets["Current trips"] = read_sumo_data(file)
            datasets["Optimized trips"] = read_sumo_data(file)
    helper = datasets["Current emissions"]
    helper = helper[["Simulation timestep", "Edge", "Amount"]]
    helper = (
        helper.groupby(["Simulation timestep", "Edge"])
        .agg({"Amount": "sum"})
        .reset_index()
    )
    datasets["Current edge noise"] = datasets["Current edge noise"].merge(
        right=helper, on=["Simulation timestep", "Edge"]
    )
    # helper = datasets["Current emissions"]
    # helper = helper[["Simulation timestep", "Lane", "Amount"]]
    # helper = (
    #     helper.groupby(["Simulation timestep", "Lane"])
    #     .agg({"Amount": "sum"})
    #     .reset_index()
    # )
    # datasets["Current lane noise"] = datasets["Current edge noise"].merge(
    #     right=helper, on=["Simulation timestep", "Lane"]
    # )

    return datasets


if __name__ == "__main__":
    runSimulation()
    data = aggregateOutputs()
