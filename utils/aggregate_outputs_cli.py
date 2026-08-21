import argparse
import os

from utils.helpers import (
    _result_data_path, aggregate_emissions_to_cells, aggregate_outputs,
    preprocess_output_resolution,
)


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
        "--aq-grid-path",
        type=str,
        help=(
            "AQ_grid.geojson used to create emission_results_cells.csv. "
            "If omitted, it is searched for in parent folders."
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
    grid_path = parsed.aq_grid_path
    if grid_path is None:
        folder = os.path.abspath(parsed.sumo_xml_folder)
        while True:
            candidate = os.path.join(folder, "AQ_grid.geojson")
            if os.path.exists(candidate):
                grid_path = candidate
                break
            parent = os.path.dirname(folder)
            if parent == folder:
                break
            folder = parent

    if parsed.preprocess_only:
        if parsed.resolution_mins is None:
            raise SystemExit("--preprocess-only requires --resolution-mins")
        preprocess_output_resolution(parsed.sumo_xml_folder, parsed.resolution_mins)
        if grid_path is not None:
            suffix = f"_res{parsed.resolution_mins}min"
            emissions_path, _ = _result_data_path(parsed.sumo_xml_folder, "emission_results", suffix)
            aggregate_emissions_to_cells(
                emissions_path, grid_path,
                os.path.join(parsed.sumo_xml_folder, "emission_results_cells.csv"),
            )
        return
    aggregate_outputs(
        parsed.sumo_net_path, parsed.sumo_xml_folder,
        erase_xml=parsed.erase_xml,
        resolution_mins=parsed.resolution_mins,
        aq_grid_path=grid_path,
    )


if __name__ == "__main__":
    main()
