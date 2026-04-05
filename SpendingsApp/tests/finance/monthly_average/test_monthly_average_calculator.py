import unittest
from SpendingsApp.finance.monthly_average.monthly_average_calculator import MonthlyAverageCalculator


class TestMonthlyAverageCalculator(unittest.TestCase):

    def make_calculator(self) -> MonthlyAverageCalculator:
        return MonthlyAverageCalculator()

    def test_calculate_should(self) -> None:
        calculator = self.make_calculator()

        actual = calculator.calculate_monthly_average()

        self.assertEqual(actual, 1)
