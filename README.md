# Water Quality Checker

A small command-line tool that reads water sample measurements from a
CSV file and checks each one against U.S. EPA benchmarks. It prints a
pass/fail report per sample and a short summary at the end.

**Note: the included `samples.csv` is synthetic example data made up
to demonstrate the tool. These are not real measurements from the
Bronx River or anywhere else.**

## How to run

```bash
python water_quality.py               # uses samples.csv
python water_quality.py my_data.csv   # uses your own file
```

Requires Python 3. No extra packages.

## Tests

Run from the project directory:

```bash
python -m unittest test_water_quality.py
```

12 tests, using only the standard library. They cover each parameter
against its EPA benchmark, including the exact boundary values (pH
6.5 and 8.5, nitrate 10.0, dissolved oxygen 5.0), a clean sample, a
sample with one bad value, a sample with a missing value, and loading
the sample file.

## What it checks

| Parameter | Benchmark | Source |
| --- | --- | --- |
| pH | 6.5 - 8.5 | EPA National Secondary Drinking Water Regulations |
| Nitrate (as N) | at most 10 mg/L | EPA Maximum Contaminant Level (MCL) |
| Dissolved oxygen | at least 5 mg/L | EPA recommended minimum for aquatic life |
| Total phosphorus | at most 0.1 mg/L | EPA recommended criterion for streams |
| Turbidity | at most 5 NTU | EPA drinking-water MCL |

## Your own data

Use the same columns as `samples.csv`:

```
site,date,ph,dissolved_oxygen_mg_l,nitrate_mg_l,total_phosphorus_mg_l,turbidity_ntu
```

One row per sample. Missing or non-numeric values count as a failure
for that parameter.

## Example output

```
Checked 6 samples from samples.csv

Bronx River - 180th St (2026-11-07): PASS
Bronx River - Bronx Park (2026-11-07): FAIL - dissolved_oxygen_mg_l out of range
Bronx River - West Farms (2026-11-07): FAIL - turbidity_ntu out of range
Bronx River - Starlight Park (2026-11-07): FAIL - total_phosphorus_mg_l out of range
Bronx River - Hunts Point (2026-11-07): FAIL - total_phosphorus_mg_l, turbidity_ntu out of range
Bronx River - Soundview (2026-11-07): PASS

Summary: 2/6 samples pass all benchmarks.
Most common problem: turbidity_ntu (2 sample(s))
```
