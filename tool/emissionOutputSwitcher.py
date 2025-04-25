import sys
import xml.etree.ElementTree as ET

try:
    EMISSION_FILE_NAME = sys.argv[1]
    SUMOCFG_FILE = sys.argv[2]
except:
    sys.exit("Please provide the emission output and SUMO config file names as arguments.")

def main():
    configXml = ET.parse(SUMOCFG_FILE)
    tree = configXml.getroot()
    output = tree.find("output")
    emissionOutput = output.find("emission-output")
    emissionOutput.set("value", "simulation_output/" + EMISSION_FILE_NAME)
    configXml.write(SUMOCFG_FILE)

if __name__ == "__main__":
    sys.exit(main())