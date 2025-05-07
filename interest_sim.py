import typing
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")

TIME_INTERVAL = 0  # seconds


def calculate_monthly_interest(balance: float, monthly_interest_rate: float) -> float:
    """Calculate the interest for the current balance."""
    return balance * monthly_interest_rate


def calculate_interest(
    principal: typing.Union[float, int] = 14623,
    repayment: typing.Union[float, int] = 100,
    downpayment: typing.Union[float, int] = 0,
    annual_interest_rate: float = 0.07,
    months: int = 12,
) -> None:
    """
    Simulate interest calculation over time.

    Args:
        principal: Initial loan amount.
        repayment: Monthly repayment amount.
        downpayment: Initial payment to reduce the principal.
        annual_interest_rate: Annual interest rate as a decimal (e.g., 0.07 for 7%).
        months: Number of months to simulate. Use 0 for indefinite simulation.
    """
    if repayment <= 0 or annual_interest_rate < 0:
        logging.error("Repayment must be positive and interest rate cannot be negative.")
        return

    balance = principal - downpayment
    monthly_interest_rate = annual_interest_rate / 12
    month_counter = 0

    while months == 0 or month_counter < months:
        if balance <= 0:
            logging.info("Loan fully repaid!")
            break

        month_counter += 1
        interest = calculate_monthly_interest(balance, monthly_interest_rate)
        balance += interest - repayment

        logging.info(f"Month: {month_counter}")
        logging.info(f"Interest: {interest:.2f}")
        logging.info(f"Remaining Balance: {balance:.2f}\n")

        time.sleep(TIME_INTERVAL)


if __name__ == "__main__":
    logging.info("Starting interest calculation...")
    calculate_interest(repayment=100, months=0)