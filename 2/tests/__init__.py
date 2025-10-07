def calculate_credit(
    amount: float, months: float, rate: float
) -> tuple[float, float, float]:
    if amount <= 0 or months <= 0 or rate < 0:
        raise ValueError("Все значения должны быть положительными")

    if rate == 0:
        payment = amount / months
        return payment, amount, 0.0

    monthly_rate = rate / 12 / 100
    payment = (amount * monthly_rate * (1 + monthly_rate) ** months) / (
        (1 + monthly_rate) ** months - 1
    )
    total = payment * months
    return payment, total, total - amount


def calculate_deposit(amount: float, months: float, rate: float) -> tuple[float, float]:
    if amount <= 0 or months <= 0 or rate < 0:
        raise ValueError("Все значения должны быть положительными")

    profit = amount * (rate / 100) * (months / 12)
    return profit, amount + profit
