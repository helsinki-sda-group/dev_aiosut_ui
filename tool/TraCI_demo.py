from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import traci
from sumolib import checkBinary
import randomTrips

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")

def run(args):
    teleports = []
    try:
        FILE = args[0]
        SIMULATION_END = int(args[1])
        AREA = args[2]
    except:
        FILE = 0
        SIMULATION_END = 600
        AREA = "kamppi"
    while traci.simulation.getTime() < SIMULATION_END:
        traci.simulationStep()
        teleports.append(traci.simulation.getStartingTeleportNumber())

    with open(f"tool/{AREA}/simulation_output/teleports_{FILE}.csv","w") as f:
        f.write(f"timestep,teleports\n")
        for i in range(len(teleports)):
            f.write(f"{i},{teleports[i]}\n")
    sys.stdout.flush()
    traci.close()


def get_options():
    """define options for this script and interpret the command line"""
    optParser = optparse.OptionParser()
    optParser.add_option("--gui", action="store_true",
                         default=False, help="run the GUI version of sumo")
    optParser.add_option("--device.battery.probability 0.2", action="store_true",
                         default=False, help="electrify the traffic by 20%")
    options, args = optParser.parse_args()
    return options,args


if __name__ == "__main__":
    options,args = get_options()
    # Run in GUI
    if options.gui:
        sumoBinary = checkBinary('sumo-gui')
        traci.start([sumoBinary, '-c', 'tool/kamppi/kamppi.sumocfg'])
    # Run in CLI
    else:
        traci.start(["sumo", '-c', 'tool/kamppi/kamppi.sumocfg'])
    run(args)
