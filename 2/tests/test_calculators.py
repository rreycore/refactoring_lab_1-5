import pytest
from calculators import calculate_credit, calculate_deposit


class TestCreditCalculator:
    def test_standard_case(self):
        payment, total, overpayment = calculate_credit(100000, 12, 15)
        assert round(payment, 2) == 9025.83
        assert round(total, 2) == 108309.97  # Исправлено ожидаемое значение
        assert round(overpayment, 2) == 8309.97

    def test_zero_interest(self):
        payment, total, overpayment = calculate_credit(100000, 12, 0)
        assert round(payment, 2) == 8333.33
        assert round(total, 2) == 100000.00
        assert round(overpayment, 2) == 0.00

    def test_short_term(self):
        payment, total, overpayment = calculate_credit(100000, 1, 12)
        assert round(payment, 2) == 101000.00
        assert round(total, 2) == 101000.00
        assert round(overpayment, 2) == 1000.00

    def test_invalid_input(self):
        with pytest.raises(ValueError):
            calculate_credit(-100000, 12, 15)
        with pytest.raises(ValueError):
            calculate_credit(100000, -12, 15)
        with pytest.raises(ValueError):
            calculate_credit(100000, 12, -15)


class TestDepositCalculator:
    def test_standard_case(self):
        profit, total = calculate_deposit(100000, 12, 8)
        assert round(profit, 2) == 8000.00
        assert round(total, 2) == 108000.00

    def test_zero_interest(self):
        profit, total = calculate_deposit(100000, 12, 0)
        assert round(profit, 2) == 0.00
        assert round(total, 2) == 100000.00

    def test_short_term(self):
        profit, total = calculate_deposit(100000, 6, 8)
        assert round(profit, 2) == 4000.00
        assert round(total, 2) == 104000.00

    def test_invalid_input(self):
        with pytest.raises(ValueError):
            calculate_deposit(-100000, 12, 8)
        with pytest.raises(ValueError):
            calculate_deposit(100000, -12, 8)
        with pytest.raises(ValueError):
            calculate_deposit(100000, 12, -8)
