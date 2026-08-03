import argparse

from utils.helpers import aggregate_outputs, preprocess_output_resolution


def parse_args(args=None):
    parser = argparse.ArgumentParser(
        description="Convert SUMO XML outputs and optionally aggregate result CSVs."
    )
    parser.add_argument(
        "--sumo-net-path",
        type=str,
        default="simulation/scenarios/vihdintie/vihdintie_trimmed.net.xml",
        help="Path to the SUMO network file.",
    )
    parser.add_argument(
        "--sumo-xml-folder",
        type=str,
        default="simulation/scenarios/vihdintie/regular_autumn_weekday/baseline",
        help="Folder containing SUMO XML output files or existing result CSV files.",
    )
    parser.add_argument(
        "--erase-xml",
        action="store_true",
        help="Erase the original XML files after conversion to CSV.",
    )
    parser.add_argument(
        "--resolution-mins",
        "--resolution_mins",
        type=int,
        help=(
            "Also create emission_results_resNmin.csv.gz and "
            "edge_noise_results_resNmin.csv.gz."
        ),
    )
    parser.add_argument(
        "--preprocess-only",
        action="store_true",
        help="Aggregate existing CSV/CSV.GZ files without parsing SUMO XML.",
    )
    return parser.parse_args(args)


def main(args=None) -> None:
    parsed = parse_args(args)
    if parsed.preprocess_only:
        if parsed.resolution_mins is None:
            raise SystemExit("--preprocess-only requires --resolution-mins")
        preprocess_output_resolution(parsed.sumo_xml_folder, parsed.resolution_mins)
        return
    aggregate_outputs(
        parsed.sumo_net_path,
        parsed.sumo_xml_folder,
        erase_xml=parsed.erase_xml,
        resolution_mins=parsed.resolution_mins,
    )


if __name__ == "__main__":
    main()
