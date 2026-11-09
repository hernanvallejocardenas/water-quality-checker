"""Unit tests for water_quality.py.

Run from the project directory with:
    python -m unittest test_water_quality.py
"""

import os
import unittest

import water_quality as wq

SAMPLES = os.path.join(os.path.dirname(__file__), "samples.csv")


class TestCheckValue(unittest.TestCase):
    """Each parameter against its EPA benchmark, including the boundaries."""

    def test_ph_in_range_passes(self):
        self.assertTrue(wq.check_value("ph", 7.2))

    def test_ph_below_minimum_fails(self):
        self.assertFalse(wq.check_value("ph", 6.4))

    def test_ph_above_maximum_fails(self):
        self.assertFalse(wq.check_value("ph", 8.6))

    def test_ph_at_boundaries_passes(self):
        self.assertTrue(wq.check_value("ph", 6.5))
        self.assertTrue(wq.check_value("ph", 8.5))

    def test_dissolved_oxygen_minimum(self):
        self.assertTrue(wq.check_value("dissolved_oxygen_mg_l", 5.0))
        self.assertFalse(wq.check_value("dissolved_oxygen_mg_l", 4.9))

    def test_nitrate_maximum(self):
        self.assertTrue(wq.check_value("nitrate_mg_l", 10.0))
        self.assertFalse(wq.check_value("nitrate_mg_l", 10.1))

    def test_phosphorus_maximum(self):
        self.assertTrue(wq.check_value("total_phosphorus_mg_l", 0.1))
        self.assertFalse(wq.check_value("total_phosphorus_mg_l", 0.11))

    def test_turbidity_maximum(self):
        self.assertTrue(wq.check_value("turbidity_ntu", 5.0))
        self.assertFalse(wq.check_value("turbidity_ntu", 5.1))


class TestCheckSample(unittest.TestCase):
    """A whole sample row: clean, one bad value, one missing value."""

    def clean_row(self):
        return {
            "site": "Test Site",
            "date": "2026-11-07",
            "ph": "7.2",
            "dissolved_oxygen_mg_l": "8.1",
            "nitrate_mg_l": "4.2",
            "total_phosphorus_mg_l": "0.04",
            "turbidity_ntu": "2.1",
        }

    def test_clean_sample_has_no_failures(self):
        self.assertEqual(wq.check_sample(self.clean_row()), [])

    def test_one_bad_value_is_reported(self):
        row = self.clean_row()
        row["nitrate_mg_l"] = "12.0"
        self.assertEqual(wq.check_sample(row), ["nitrate_mg_l"])

    def test_missing_value_counts_as_failure(self):
        row = self.clean_row()
        row["ph"] = ""
        self.assertEqual(wq.check_sample(row), ["ph"])


class TestLoadSamples(unittest.TestCase):
    def test_loads_sample_file(self):
        samples = wq.load_samples(SAMPLES)
        self.assertEqual(len(samples), 6)
        self.assertEqual(samples[0]["site"], "Bronx River - 180th St")


if __name__ == "__main__":
    unittest.main()
