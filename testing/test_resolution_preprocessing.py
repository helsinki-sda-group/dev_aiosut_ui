import os
import tempfile
import unittest

import pandas as pd

from utils.aggregate_outputs_cli import parse_args
from utils.helpers import (
    _aggregate_result_resolution,
    _result_data_path,
    preprocess_output_resolution,
)


class ResolutionPreprocessingTests(unittest.TestCase):
    def test_emissions_are_aggregated_per_vehicle_edge_and_minute(self):
        data = pd.DataFrame(
            {
                "Simulation timestep": [1.0, 20.0, 61.0],
                "Edge": ["e1", "e1", "e1"],
                "Vehicle": ["v1", "v1", "v1"],
                "Mobility mode": pd.Categorical(["car", "car", "car"], categories=["car", "bus"]),
                "Mobility flow": [1, 1, 1],
                "Speed": [10.0, 20.0, 30.0],
                "Carbon monoxide": [2.0, 3.0, 5.0],
                "Longitude": [24.0, 24.0, 24.0],
            }
        )

        result = _aggregate_result_resolution(data, "emission_results", 1)

        self.assertEqual(len(result), 2)
        self.assertEqual(result["Simulation timestep"].tolist(), [0, 60])
        self.assertEqual(result["Mobility flow"].tolist(), [2, 1])
        self.assertEqual(result["Speed"].tolist(), [15.0, 30.0])
        self.assertEqual(result["Carbon monoxide"].tolist(), [5.0, 5.0])

    def test_edge_noise_is_averaged_per_edge_and_minute(self):
        data = pd.DataFrame(
            {
                "Simulation timestep": [0.0, 30.0, 60.0],
                "Edge": ["e1", "e1", "e1"],
                "Noise": [50.0, 70.0, 80.0],
                "Name": ["Road", "Road", "Road"],
            }
        )

        result = _aggregate_result_resolution(data, "edge_noise_results", 1)

        self.assertEqual(len(result), 2)
        self.assertEqual(result["Simulation timestep"].tolist(), [0, 60])
        self.assertEqual(result["Noise"].tolist(), [60.0, 80.0])

    def test_preprocessor_writes_expected_gzip_files(self):
        with tempfile.TemporaryDirectory() as output_dir:
            emissions = pd.DataFrame(
                {
                    "Simulation timestep": [0.0],
                    "Edge": ["e1"],
                    "Vehicle": ["v1"],
                    "Mobility mode": ["car"],
                    "Mobility flow": [1],
                }
            )
            noise = pd.DataFrame(
                {"Simulation timestep": [0.0], "Edge": ["e1"], "Noise": [55.0]}
            )
            emissions.to_csv(
                os.path.join(output_dir, "emission_results.csv.gz"), index=False
            )
            noise.to_csv(
                os.path.join(output_dir, "edge_noise_results.csv.gz"), index=False
            )

            paths = preprocess_output_resolution(output_dir, 1)

            self.assertEqual(
                {os.path.basename(path) for path in paths},
                {
                    "emission_results_res1min.csv.gz",
                    "edge_noise_results_res1min.csv.gz",
                },
            )
            result_path = os.path.join(
                output_dir, "emission_results_res1min.csv.gz"
            )
            self.assertEqual(pd.read_csv(result_path).shape[0], 1)

    def test_result_path_prefers_minute_file_and_falls_back(self):
        with tempfile.TemporaryDirectory() as output_dir:
            raw = os.path.join(output_dir, "emission_results.csv.gz")
            open(raw, "a").close()
            self.assertEqual(
                _result_data_path(output_dir, "emission_results")[0], raw
            )

            minute = os.path.join(
                output_dir, "emission_results_res1min.csv.gz"
            )
            open(minute, "a").close()
            self.assertEqual(
                _result_data_path(output_dir, "emission_results")[0], minute
            )

    def test_cli_accepts_both_resolution_spellings(self):
        self.assertEqual(
            parse_args(["--resolution-mins", "1"]).resolution_mins, 1
        )
        self.assertEqual(
            parse_args(["--resolution_mins", "5"]).resolution_mins, 5
        )

    def test_resolution_must_be_positive(self):
        with self.assertRaisesRegex(ValueError, "positive integer"):
            preprocess_output_resolution("unused", 0)


if __name__ == "__main__":
    unittest.main()
