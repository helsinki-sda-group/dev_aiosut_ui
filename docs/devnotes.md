# Milestones

M1. Visualize the outputs (baseline/optimized) for Couscous model (denoted as `vihdintie_small`).

M2. Launch the model for AIOSUT area (denoted as `vihdintie_large`).

M3. Train the model for different scenarios (season/time of week/demand/priorities).

# M1 tasks

## Notes

- Traffic and Air Quality tabs use the data from `.csv.gz` files which are raw SUMO outputs on emissions, trips and noise preprocessed with a function `aggregate_outputs()` from module `utils/helpers`. Preprocessing also extract edge/lane coordinates from `baseline.net.xml` and bakes them into `.csv.gz` files. 
- Current tool uses the following xml files from SUMO outputs: edge noise, trip output, emissions. To get edge noise from SUMO, one needs to specify `edgeData` in `add.xml` (see the example in `dev_aiosut_ui` repo). Trip and emission outputs are specified in config.sumocfg.
- `trip_results.csv` contains aggregated information per trip on lost time, travel time, mobility mode and emissions, obtained from tripinfo.xml.
- `emissions_results.csv` contains per-step emissions, noise and speed data, including edge location and name.
- Summary tab also pulls data from  `.csv.gz` files using `get_data()` function. This function aggregates the observables for the whole simulation period. 

## Questions to discuss
- [ ] How to visualize priorities of objectives? How about dropdown list Traffic 0.4, AQ 0.3, Liv  0.3?
- [ ] What is baseline? 
- [x] What do we want to show in summary? Now it is mobility mode distribution, average travel time, respirable particles (?). According to Linsen's slides, it may be driving percentage (baseline vs optimized), average speed (baseline vs optimized), air quality (PM2.5 / BC / Ntot), normalized livability. 
- [x] The tool assumes that mobility modes are represented by two types of cars: fuel and electric. Which mobility modes are supported now in the model (and which do we want to show)? Pedestrians, bicycles, private cars, buses. No different types of cars (?).
- [x] Which observables to visualize for livability? Relocation rate, demographics of the agents. Changing livability values (?). 
- [ ] Does each combination of priorities already has corresponding SUMO output data (namely, `emission_results.xml`, `trip_results.xml`,`edge_noise_results.xml`)? 
  
## Description of the code base (devnotes)
- `callbacks.py`, `show_graphs` - main plotting logic, uses `utils.helpers.get_data()`, which read the data from `csv.gz` files.
- `helpers.aggregate_outputs` creates `csv` from SUMO `xml` files with `_parse` functions. New parsers need to be implemented for new types of input files.


## Modifications
- For `vihdintie_trimmed.net.xml`, original location tag was replaced with `<location netOffset="-379248.78,-6676018.56" convBoundary="332.66,824.20,4293.93,6190.00" origBoundary="24.818413,60.203837,24.905479,60.259108" projParameter="+proj=utm +zone=35 +ellps=WGS84 +datum=WGS84 +units=m +no_defs"/>` for correct `pyproj` processing.
- All edges of Vihdintie network are unnamed.








  


