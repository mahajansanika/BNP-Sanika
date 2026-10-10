from datetime import date, timedelta

def calculate_adjusted_maturity(
    calc_date: date, 
    contractual_date: date, 
    early_exit_prob: float
) -> date:

    remaining_days = (contractual_date - calc_date).days
    adjusted_days = round(remaining_days * (1.0 - early_exit_prob))
    raw_adjusted_date = calc_date + timedelta(days=adjusted_days)

    return max(calc_date, min(contractual_date, raw_adjusted_date))