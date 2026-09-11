# dev_aiosut_ui

AioSUT is a RCF-funded project about developing an AI-based optimization tool for city planning. In this repository reisdes the development code for the AioSUT tool's user interface.

## User Guide

Run the visualization with the existing edge-based air-quality view using
`python -m new_app --edge` (also the default), or with polygon cell results from
`emission_results_cells.csv` and `AQ_grid.geojson` using `python -m new_app --cell`. Check `commands.sh` for more examples of commands.

1. Install the following pre-requisites:
   - **Python**: Download the latest Python from [Python's official website](https://www.python.org/downloads/). Pip is recommended as the package installer.
   - **Simulation for Urban MObility (SUMO)**: Follow the installation instructions from [SUMO's official website.](https://www.eclipse.org/sumo/)
   - **Git for Windows, if using Windows**: Download the latest Git for Windows from [Git's official website](https://gitforwindows.org/).
2. Clone the repository
3. Run `sh commands.sh` in the command line in the root folder
4. Once the terminal has finished printing the link, click on it
5. Success!

## Developer Guide

### Contribution pipeline

The project follows a relaxed development pipeline by using issues, pull requests and a project roadmap to keep track of features, bugs, version releases and milestones.

1. Check out [the project roadmap](https://github.com/orgs/helsinki-sda-group/projects/3). P0 denotes the most urgent issues to be solved for the next milestone, P1 the next most urgent and so on. Milestones are used to keep track of the project-related deadlines, such as the workshops. Version releases denote the overall progress of the UI.
2. Pick an issue to work on by assigning yourself to it.
3. Update the issue and project roadmap. Use [the semantic versioning guidelines](https://semver.org/) for the release version column.
4. Solve the issue as you see fit and submit a pull request.
5. Wait patiently until the pull request is merged.
6. Once merged, update the end date to the roadmap and enjoy your work's results! Sara will handle the rest of the roadmap, milestones and version releases ater you.
7. Remember to pass the good on: check and close other people's pull requests when you can!

### Structure of the repository

- `commands.sh` contains the command line script used to run the tool for the first time.
- `LICENSE` contains the info about the license this project is distributed under.
- `requirements.txt` contains a list of the required Python libraries for running the tool. The command line script uses this list to install them via the package installer.
- `app.ipynb` is used as an interface for running the simulation tool and analysing the results.
- The `simulation` folder contains the simulation loop as a whole.
  - `functions.py` contains all the functions needed for runing SUMO simulations and fetching the results for visualization.
  - The sub-folders of the `simulation` folder, eg. `kamppi`, are area folders that contain the simulation configurations and simulation outputs for each area. The configurations consist mainly of three files:
    - the road network used in the simulation, `.net.xml`
    - the grid boundary coordinates for `--cell` visualization mode, `AQ_grid.geojson`
    - the routes of the vehicles, `.rou.xml`
    - file configurations for the simulation, `.sumocfg`
    - In each area folder, there is a sub-folder `output` for the simulation outputs.

### Preparing simulation data (CSV.GZ files)

The UI reads pre-processed `.csv.gz` files from `simulation/scenarios/<area>/<scenario>/`. These are produced from raw SUMO output by running a simulation via `run_simulation()` in `utils/helpers.py`, or by manually calling `aggregate_outputs()` on an existing SUMO output folder (`utils/aggregate_outputs_cli.py`). The full pipeline is:

#### 1. Run the SUMO simulation

SUMO must be installed and the `SUMO_HOME` environment variable must point to its installation directory. The simulation is run for 3600 seconds (1 hour) at 1-second time resolution. It produces two raw XML output files in the scenario output folder:

- `emission_results.xml` — per-vehicle, per-second emissions (CO₂‚, CO, HC, NOx, PMx), speed, noise, fuel/electricity consumption, and vehicle class.
- `trip_results.xml` — per-trip travel time, lost time, and route information.
- `edge_noise_results.xml` — per-edge noise levels aggregated by the `add.xml` additional file.

The emission output uses the **HBEFA4** model with two vehicle types defined in `rou.xml`:
- `HBEFA4/PC_petrol_ltECE` — petrol passenger car (pre-ECE standard)
- `HBEFA4/PC_BEV` — battery electric vehicle (zero tailpipe emissions)

#### 2. Convert XML outputs to CSV.GZ

After the simulation finishes, call `aggregate_outputs()` with the paths to the baseline network file and the scenario output folder:

```python
from utils.helpers import aggregate_outputs

aggregate_outputs(
    net_path="simulation/scenarios/kamppi/baseline_net.xml",
    full_output_folder="simulation/scenarios/kamppi/regular_autumn_weekday/baseline",
)
```

This function:
1. Parses `baseline_net.xml` to extract edge/lane geometry (coordinates, edge IDs).
2. For each XML file in the output folder:
   - Parses the XML into a pandas DataFrame.
   - Merges with the network geometry to attach `Longitude`, `Latitude`, and `Edge` to each record.
   - Saves the result as a gzip-compressed CSV (`.csv.gz`) alongside the original XML.
   - Deletes the raw XML file if `erase_xml=True`.

The resulting `.csv.gz` files have **1-second time resolution** (`Simulation timestep` column in seconds) and are what the UI loads at runtime. The UI then re-bins the data into the user-selected temporal resolution (1 min, 15 min, 30 min, or 60 min) on the fly. If 1-second time resolution becomes too slow for the on-the-fly visualization, use `utils.aggregate_outputs_cli` with parameters `--resolution-mins 1` to create preprocessed files with 1-minute resolution (see below).

Script `utils/aggregate_outputs_cli.py` can be used to produce `csv` and `csv.gz` files through command line from the existing SUMO outputs. In this case, files will be read from and write to `--sumo-xml-folder` path.

To create the faster one-minute files while converting XML, pass `--resolution-mins 1`:

```shell
python -m utils.aggregate_outputs_cli --sumo-net-path <network.xml> --sumo-xml-folder <output-folder> --resolution-mins 1
```

To preprocess existing one-second CSV or CSV.GZ files without reading XML, use:

```shell
python -m utils.aggregate_outputs_cli --sumo-xml-folder <output-folder> --preprocess-only --resolution-mins 1
```

This writes `emission_results_res1min.csv.gz` and `edge_noise_results_res1min.csv.gz`. Emissions are grouped per vehicle, edge, mobility mode, and minute: additive values such as emissions and mobility flow are summed, while speed and noise are averaged. Edge noise is averaged per edge and minute. The UI automatically prefers a complete matching pair of one-minute noise/emissions files and otherwise falls back to the original files, so existing scenarios remain compatible. The underscore spelling `--resolution_mins` is also accepted.

Additionally, the file `emission_results_cells.csv` will be generated, using `AQ_grid.geojson` file with cell borders in a parent folder.

To visualize precomputed Enfuser concentrations, place
`concentration_results_cells.csv` in the scenario result folder and run:

```shell
python -m new_app --cell --concentration
```

The concentration file uses its `time` timestamps at one-minute resolution and
the `cnc_PM2_5`, `cnc_PM10`, and `cnc_NO2_gas` columns. The UI displays these as
PM2.5, PM10, and NO2 in µg/m³ and uses the same `AQ_grid.geojson` lookup as the
cell-emissions mode. Concentrations are averaged, rather than summed, when a
coarser temporal resolution is selected.

> **Note 1**. Processing of `emission_results.xml` can take a long time (dozens of minutes) for a large number of cars or a long simulation period. 

> **Note 2**. If there is an error `pyproj.exceptions.CRSError: Invalid projection: UTM: (Internal Proj Error: proj_create: unrecognized format / unknown name)`, check `projParameter` of `<location>` tag of `net.xml` file. Modify as: `projParameter="+proj=utm +zone=35 +ellps=WGS84 +datum=WGS84 +units=m +no_defs"` 

> **Note 3**. For generating `emission_results_cells.csv` for non-default `sumo-net-path` and `sumo-xml-folder`, please specify `--aq-grid-path` path to  `AQ_grid.geojson`. By default, CLI checks for it in `sumo-xml-folder` and its parent folder.

#### Expected folder structure

```
simulation/
  scenarios/
    <area>/                          # e.g. kamppi
      baseline_net.xml               # SUMO road network
      add.xml                        # additional file (noise output config)
      rou.xml                        # vehicle routes and types
      <demand>_<season>_<day>/       # e.g. regular_autumn_weekday
        baseline/
          emission_results.csv.gz
          edge_noise_results.csv.gz
          trip_results.csv.gz
        optimized_<weights>/
          emission_results.csv.gz
          edge_noise_results.csv.gz
          trip_results.csv.gz
```

## License

Distributed under the MIT License. See the `LICENSE` -file for more information.
