import argparse

from utils.helpers import aggregate_outputs

def parse_args():
    parser = argparse.ArgumentParser(description="Convert SUMO XML outputs to compressed CSV files.")
    parser.add_argument(
        "--sumo-net-path",
        type=str,
        default="simulation/scenarios/vihdintie/vihdintie_trimmed.net.xml",
        help="Path to the SUMO network file."
    )
    parser.add_argument(
        "--sumo-xml-folder",
        type=str,
        default="simulation/scenarios/vihdintie/regular_autumn_weekday/baseline",
        help="Folder containing SUMO XML output files."
    )
    parser.add_argument(
        "--erase-xml",
        action="store_true",
        help="Erase the original XML files after conversion to CSV."
    )
    return parser.parse_args()

def main() -> None:
    args = parse_args()
    aggregate_outputs(args.sumo_net_path, args.sumo_xml_folder, erase_xml=args.erase_xml)

if __name__ == "__main__":
    main()