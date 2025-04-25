# Imports and requirements
python -m pip install -r "./tool/requirements.txt"

# Python filepath for SUMO
export PYTHONPATH="$SUMO_HOME/tools:$PYTHONPATH"

# Simulation run
# Create 2 400 vehicle (20% of which electric) routes for 3 600 timesteps/seconds
python "./tool/trafficCreator.py" 2400 3600
# Assign the output location
python "./tool/emissionOutputSwitcher.py" emissions_1.xml "./tool/kamppi/kamppi.sumocfg"
# Run the simulation
# To run the simulation in GUI, add "--gui" to TraCI_demo.py
python "./tool/TraCI_demo.py" 1 3600 "kamppi"

# Convert the output file and aggregate it
python "$SUMO_HOME/tools/xml/xml2csv.py" "./tool/kamppi/simulation_output/emissions_1.xml"
python "./tool/aggregation.py"

# Visualize the emission output
python -m jupyter notebook "./tool/visualization.ipynb"