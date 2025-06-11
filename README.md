# dev_aiosut_ui

AioSUT is a RCF-funded project about developing an AI-based optimization tool for city planning. In this repository reisdes the development code for the AioSUT tool's user interface.

## User Guide

1. Install the following pre-requisites:
   - **Python**: Download the latest Python from [Python's official website](https://www.python.org/downloads/). Pip is recommended as the package installer.
   - **Simulation for Urban MObility (SUMO)**: Follow the installation instructions from [SUMO's official website.](https://www.eclipse.org/sumo/)
   - **Git for Windows, if using Windows**: Download the latest Git for Windows from [Git's official website](https://gitforwindows.org/).
2. Clone the repository
3. Run `sh commands.sh` in the command line in the root folder
4. Once the `app.ipynb` opens in the browser, run All Cells of the notebook
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

- `commands.sh` contains the command line script used to run the pipeline as a whole.
- `LICENSE` contains the info about the license this project is distributed under.
- The `tool` folder contains the tool as a whole.
  - `requirements.txt` contains a list of the required Python libraries for running the project. The command line script uses this list to install them via the package installer.
  - `aggregation.py` is used to process the raw output of SUMO into a clean dataset used for visualization.
  - `emissionOutputSwitcher.py`is used change the location of the emission output files.
  - `TraCI_demo.py` are used to configure TraCI to run SUMO and produce the results of the simulation
  - `trafficCreator.py` is used to create traffic inside the simulation.
  - `app.ipynb` is used to produce the interactive visualisation.
  - The sub-folders of the `tool` folder, eg. `kamppi`, are area folders that contain the simulation configurations and simulation outputs for each area. The configurations consist mainly of three files:
    - the road network used in the simulation, `.net.xml`
    - the routes of the vehicles, `.rou.xml`
    - file configurations for the simulation, `.sumocfg`
    - In each area folder, there is a sub-folder for the simulation outputs:
      - the full vehicle and second-level output of the simulation, `test_fcdresults.xml`
      - observed emissions, `emissions.csv` and `emissions.xml`
      - a helper file for creating other outputs, `plot_net_dump.xml`
      - teleports per timestep, `teleports.csv`
      - a cleaned dataset used for the visualization, `clean_data.csv`

## License

Distributed under the MIT License. See the `LICENSE` -file for more information.
