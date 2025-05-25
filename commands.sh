# Imports and requirements
python -m pip install -r "./tool/requirements.txt"

# Python filepath for SUMO
export PYTHONPATH="$SUMO_HOME/tools:$PYTHONPATH"

# Run the simulation
python "./simulation/functions.py"

# Run the visualization app in browser
python -m jupyter notebook "./tool/app.ipynb"