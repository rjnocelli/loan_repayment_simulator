import typing
import logging
import csv
import argparse
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")


@dataclass
class MonthlyResult:
    month: int
    interest: float
    balance: float
    accumulated_interest: float
    total_paid: float
    interest_percentage: float


def calculate_monthly_interest(balance: float, monthly_interest_rate: float) -> float:
    """Calculate the interest for the current balance."""
    return balance * monthly_interest_rate


def simulate_interest(
    principal: float,
    repayment: float,
    downpayment: float,
    annual_interest_rate: float,
    months: int,
    export_to_csv: bool = False,
    csv_filename: str = "simulation_results.csv",
) -> typing.List[MonthlyResult]:
    """
    Simulate interest calculation over time.

    Args:
        principal: Initial loan amount.
        repayment: Monthly repayment amount.
        downpayment: Initial payment to reduce the principal.
        annual_interest_rate: Annual interest rate as a decimal (e.g., 0.07 for 7%).
        months: Number of months to simulate. Use 0 for indefinite simulation.
        export_to_csv: Boolean to indicate if results should be exported to a CSV file.
        csv_filename: Name of the CSV file to export results.

    Returns:
        A list of MonthlyResult objects containing the simulation results.
    """
    if principal <= 0:
        raise ValueError("Principal must be greater than zero.")
    if downpayment < 0:
        raise ValueError("Downpayment cannot be negative.")
    if downpayment > principal:
        raise ValueError("Downpayment cannot exceed the principal.")
    if repayment <= 0 or annual_interest_rate < 0:
        raise ValueError(
            "Repayment must be positive and interest rate cannot be negative."
        )

    accumulated_interest = 0
    total_paid = 0
    balance = principal - downpayment
    monthly_interest_rate = annual_interest_rate / 12
    month_counter = 0
    results = []

    MAX_ITERATIONS = 1000  # Safeguard for infinite loops

    while months == 0 or month_counter < months:
        if balance <= 0:
            break

        if repayment <= monthly_interest_rate * balance:
            raise ValueError(
                "Repayment is too low to cover the monthly interest. Balance will grow indefinitely."
            )

        month_counter += 1
        interest = calculate_monthly_interest(balance, monthly_interest_rate)
        balance += interest - repayment
        accumulated_interest += interest
        total_paid += repayment

        # Avoid negative balance
        if balance < 0:
            total_paid += balance  # Adjust final payment
            balance = 0

        results.append(
            MonthlyResult(
                month=month_counter,
                interest=interest,
                balance=balance,
                accumulated_interest=accumulated_interest,
                total_paid=total_paid,
                interest_percentage=(accumulated_interest / total_paid * 100)
                if total_paid > 0
                else 0,
            )
        )

        if month_counter > MAX_ITERATIONS:
            raise RuntimeError(
                "Simulation exceeded maximum iterations. Check your inputs."
            )

        if export_to_csv:
            export_results_to_csv(
                results,
                csv_filename,
                principal,
                repayment,
                downpayment,
                annual_interest_rate,
                months,
            )

    return results


def export_results_to_csv(
    results: typing.List[MonthlyResult],
    filename: str,
    principal: float,
    repayment: float,
    downpayment: float,
    annual_interest_rate: float,
    months: int,
) -> None:
    """Export the simulation results to a CSV file."""
    with open(filename, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)

        # Add input parameters as the first row
        writer.writerow(
            [
                "Input Parameters",
                f"Principal: {principal}",
                f"Repayment: {repayment}",
                f"Downpayment: {downpayment}",
                f"Annual Interest Rate: {annual_interest_rate}",
                f"Months: {months}",
            ]
        )

        # Add a blank row for separation
        writer.writerow([])

        # Add headers for the results
        writer.writerow(
            [
                "Month",
                "Interest",
                "Balance",
                "Accumulated Interest",
                "Total Paid",
                "Interest Percentage",
            ]
        )

        # Write the simulation results
        for result in results:
            writer.writerow(
                [
                    result.month,
                    f"{result.interest:.2f}",
                    f"{result.balance:.2f}",
                    f"{result.accumulated_interest:.2f}",
                    f"{result.total_paid:.2f}",
                    f"{result.interest_percentage:.2f}",
                ]
            )
    logging.info(f"Results exported to {filename}")


def log_results(results: typing.List[MonthlyResult]) -> None:
    """Log the results of the simulation."""
    for result in results:
        logging.info(f"Month: {result.month}")
        logging.info(f"Interest: {result.interest:.2f}")
        logging.info(f"Remaining Balance: {result.balance:.2f}")
        logging.info(f"Accumulated Interest Paid: {result.accumulated_interest:.2f}")
        logging.info(
            f"Total Paid: {result.total_paid:.2f} | Interest: {result.interest_percentage:.2f}%\n"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Simulate loan repayment with interest."
    )
    parser.add_argument(
        "--principal", type=float, required=True, help="Initial loan amount."
    )
    parser.add_argument(
        "--repayment", type=float, required=True, help="Monthly repayment amount."
    )
    parser.add_argument(
        "--downpayment",
        type=float,
        default=0,
        help="Initial payment to reduce the principal.",
    )
    parser.add_argument(
        "--annual_interest_rate",
        type=float,
        required=True,
        help="Annual interest rate as a decimal (e.g., 0.07 for 7%).",
    )
    parser.add_argument(
        "--months",
        type=int,
        default=12,
        help="Number of months to simulate (0 for indefinite).",
    )
    parser.add_argument(
        "--export_to_csv", action="store_true", help="Export results to a CSV file."
    )
    parser.add_argument(
        "--csv_filename",
        type=str,
        default="simulation_results.csv",
        help="Name of the CSV file to export results.",
    )

    args = parser.parse_args()

    logging.info("Starting interest calculation...")
    try:
        results = simulate_interest(
            principal=args.principal,
            repayment=args.repayment,
            downpayment=args.downpayment,
            annual_interest_rate=args.annual_interest_rate,
            months=args.months,
            export_to_csv=args.export_to_csv,
            csv_filename=args.csv_filename,
        )
        log_results(results)
    except ValueError as e:
        logging.error(f"Input error: {e}")
    except RuntimeError as e:
        logging.error(f"Simulation error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
