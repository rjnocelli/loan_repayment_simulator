# Loan Repayment Simulator

This Python script simulates loan repayment with interest over a specified period. It calculates monthly interest, tracks the remaining balance, and provides detailed results for each month. The script also supports exporting the results to a CSV file for further analysis.

## Features

- Simulates loan repayment with interest over a specified number of months.
- Calculates monthly interest, accumulated interest, and total payments.
- Handles edge cases like insufficient repayment amounts.
- Exports simulation results to a CSV file.
- Accepts input parameters via command-line arguments.

## Requirements

- Python 3.7 or higher
- No additional dependencies (uses built-in Python libraries)

## Usage

Run the script from the terminal with the required arguments:

```bash
python interest_sim.py --principal <principal> --repayment <repayment> --downpayment <downpayment> --annual_interest_rate <annual_interest_rate> --months <months> [--export_to_csv] [--csv_filename <filename>]