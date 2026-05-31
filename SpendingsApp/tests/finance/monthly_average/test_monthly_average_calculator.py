import pytest
from unittest.mock import Mock
from unittest.mock import patch
from datetime import date

from SpendingsApp.utils.date_range import DateRange
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
    mock = Mock(spec=MonthlyAverageDataGateway)
    mock.get_spending_amount.return_value = 100
    return mock


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

@pytest.mark.parametrize("today, year_input", [
    (date(2025, 1, 30), 2025),
    (date(2001, 1, 1), 2001),
    (date(1999, 5, 16), 2000),
    (date(2027, 10, 10), 2050),
])
def test_calculate_shouldNotRequestAverage_IfYearIsInTheFuture(calculator: MonthlyAverageCalculator, data_gateway_mock: Mock, today: date, year_input: int) -> None:
    DateMock._today = today
    with patch(f"{TESTED_MODULE}.date", DateMock):
        category_data = CategoryData(id=1, name="Test Category")
        calculator.calculate_monthly_average(year_input, category_data)

        assert 0 == data_gateway_mock.get_spending_amount.call_count

@pytest.mark.parametrize("today, year_input", [
    (date(2025, 1, 30), 2025),
    (date(2001, 1, 1), 2001),
    (date(1999, 5, 16), 2000),
    (date(2012, 9, 23), 2050),
])
def test_calculate_ShouldReturn0_IfAverageNotPossible(calculator: MonthlyAverageCalculator, data_gateway_mock: Mock, today: date, year_input: int) -> None:
    DateMock._today = today
    with patch(f"{TESTED_MODULE}.date", DateMock):
        category_data = CategoryData(id=1, name="Test Category")
        average = calculator.calculate_monthly_average(year_input, category_data)

        assert 0 == average

@pytest.mark.parametrize("category_data", [
    CategoryData(id=42, name="Test Category"),
    CategoryData(id=0, name="Bla"),
    CategoryData(id=305, name="Thomas Müller"),

])
def test_calculate_ShouldUseRightCategory(calculator: MonthlyAverageCalculator, data_gateway_mock: Mock, category_data: CategoryData) -> None:
    DateMock._today = date(2025, 1, 30)
    with patch(f"{TESTED_MODULE}.date", DateMock):
        calculator.calculate_monthly_average(2024, category_data)

        assert 1 == data_gateway_mock.get_spending_amount.call_count
        call_args = data_gateway_mock.get_spending_amount.call_args.args
        assert 2 == len(call_args)
        expected = category_data
        actual = call_args[1]
        assert expected == actual


@pytest.mark.parametrize("year, today, amount, expected_average", [
    (2025, date(2025, 6, 23), 2000, 400),
    (1999, date(1999, 2, 1), 604, 604),
    (2023, date(2023, 12, 31), 789, 71.72727272727273),
    (2011, date(2011, 4, 1), 921, 307),
    (2008, date(2009, 6, 23), 13400, 1116.666666666667),
    (2001, date(2026, 1, 1), 12398, 1033.166666666667),
])
def test_calculate_ShouldReturnRightAverage(
        calculator: MonthlyAverageCalculator, data_gateway_mock: Mock, year: int, today: date, amount: float, expected_average: float) -> None:
    DateMock._today = today
    with patch(f"{TESTED_MODULE}.date", DateMock):
        category_data = CategoryData(id=42, name="Test Category")
        data_gateway_mock.get_spending_amount.return_value = amount

        actual_average = calculator.calculate_monthly_average(year, category_data)

        assert expected_average == pytest.approx(actual_average, abs=0.001)