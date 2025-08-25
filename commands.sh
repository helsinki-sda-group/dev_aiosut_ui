# Imports and requirements
python -m pip install -r "requirements.txt"

# Python filepath for SUMO
export PYTHONPATH="$SUMO_HOME/tools:$PYTHONPATH"

# Run the simulation
# python -c 'import ./utils/helpers as uh; uh.run_simulation()'

# Run the visualization app
python -m "new_app.py"

# Finally, click on the link in the terminal output!