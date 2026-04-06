import pytest
from unittest.mock import Mock
from unittest.mock import patch
from datetime import date

from SpendingsApp.src.date_range import DateRange
from SpendingsApp.finance.category_data import CategoryData

from SpendingsApp.finance.monthly_average.monthly_average_calculator import MonthlyAverageCalculator
from SpendingsApp.finance.monthly_average.monthly_average_data_gateway import MonthlyAverageDataGateway

TESTED_MODULE = str(MonthlyAverageCalculator.__module__)

class DateMock(date):
    _today: date = date(2025, 1, 1)

    @classmethod
    def today(cls):
        return cls._today

@pytest.fixture
def data_gateway_mock() -> Mock:
    return Mock(spec=MonthlyAverageDataGateway)


@pytest.fixture
def calculator(data_gateway_mock: Mock) -> MonthlyAverageCalculator:
    return MonthlyAverageCalculator(data_gateway_mock)


@pytest.mark.parametrize("year", [
    (-1),
    (-10),
    (-2025)
])
def test_calculate_shouldRaiseException_IfYearIsNegative(calculator: MonthlyAverageCalculator, year: int) -> None:
    category_data = CategoryData(id=1, name="Test Category")
    with pytest.raises(ValueError):
        calculator.calculate_monthly_average(year, category_data)

@pytest.mark.parametrize("year_input, today, date_range", [
    (2010, date(2010, 4, 9), DateRange(date(2010, 1, 1), date(2010, 3, 31))),
    (2030, date(2030, 12, 31), DateRange(date(2030, 1, 1), date(2030, 11, 30))),
    (1999, date(2012, 10, 10), DateRange(date(1999, 1, 1), date(1999, 12, 31))),
])
def test_calculate_shouldRequestRightDateRange(calculator: MonthlyAverageCalculator, data_gateway_mock: Mock,  year_input: int, today: date, date_range: DateRange) -> None:
    DateMock._today = today
    with patch(f"{TESTED_MODULE}.date", DateMock):
        DateMock._today = today

        category_data = CategoryData(id=1, name="Test Category")
        calculator.calculate_monthly_average(year_input, category_data)

        assert 1 == data_gateway_mock.get_spending_amount.call_count
        call_args = data_gateway_mock.get_spending_amount.call_args.args
        assert 2 == len(call_args)
        expected = date_range
        actual = call_args[0]
        assert expected == actual
