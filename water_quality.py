#!/usr/bin/env python3
"""
Water Quality Checker

Reads water sample measurements from a CSV file and checks each one
against U.S. EPA benchmarks. Prints a pass/fail report per sample
and a short summary at the end.

Usage:
    python water_quality.py               # uses samples.csv
    python water_quality.py my_data.csv   # uses your own file

CSV columns: site, date, ph, dissolved_oxygen_mg_l, nitrate_mg_l,
             total_phosphorus_mg_l, turbidity_ntu
"""

import csv
import sys
from collections import Counter

# EPA benchmarks. Sources:
#   pH 6.5-8.5: EPA National Secondary Drinking Water Regulations
#   Nitrate (as N) <= 10 mg/L: EPA Maximum Contaminant Level (MCL)
#   Dissolved oxygen >= 5 mg/L: EPA recommended minimum for aquatic life
#   Total phosphorus <= 0.1 mg/L: EPA recommended criterion for streams
#   Turbidity <= 5 NTU: EPA drinking-water MCL
THRESHOLDS = {
    "ph": (6.5, 8.5),
    "dissolved_oxygen_mg_l": (5.0, None),   # minimum only
    "nitrate_mg_l": (None, 10.0),           # maximum only
    "total_phosphorus_mg_l": (None, 0.1),   # maximum only
    "turbidity_ntu": (None, 5.0),           # maximum only
}

PARAMETERS = list(THRESHOLDS)


def check_value(name, value):
    """Return True if value is within the EPA benchmark for this parameter."""
    low, high = THRESHOLDS[name]
    if low is not None and value < low:
        return False
    if high is not None and value > high:
        return False
    return True


def check_sample(row):
    """Check one sample (a dict from the CSV). Returns failed parameter names."""
    failed = []
    for name in PARAMETERS:
        try:
            value = float(row[name])
        except (TypeError, ValueError):
            failed.append(name)  # missing or non-numeric counts as a failure
            continue
        if not check_value(name, value):
            failed.append(name)
    return failed


def load_samples(path):
    """Read the CSV file into a list of dicts, one per sample."""
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "samples.csv"
    samples = load_samples(path)

    failures = Counter()
    passing = 0

    print(f"Checked {len(samples)} samples from {path}\n")
    for row in samples:
        failed = check_sample(row)
        if failed:
            failures.update(failed)
            print(f"{row['site']} ({row['date']}): FAIL - "
                  f"{', '.join(failed)} out of range")
        else:
            passing += 1
            print(f"{row['site']} ({row['date']}): PASS")

    print(f"\nSummary: {passing}/{len(samples)} samples pass all benchmarks.")
    if failures:
        worst, count = failures.most_common(1)[0]
        print(f"Most common problem: {worst} ({count} sample(s))")


if __name__ == "__main__":
    main()
