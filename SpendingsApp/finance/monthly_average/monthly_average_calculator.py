
from datetime import date, timedelta

from SpendingsApp.finance.category_data import CategoryData
from SpendingsApp.src.date_range import DateRange
from .monthly_average_data_gateway import MonthlyAverageDataGateway


class MonthlyAverageCalculator:
    def __init__(self, data_gateway: MonthlyAverageDataGateway):
        self._data_gateway = data_gateway
        

    def calculate_monthly_average(self, year: int, category: CategoryData) -> float:
        if year < 0:
            raise ValueError(f"Year cannot be negative but was '{year}'.")

        date_range = self._calc_date_range(year)
        self._data_gateway.get_spending_amount(date_range, None)

        return 1
    
    def _calc_date_range(self, requested_year: int) -> DateRange:
        today = date.today()
        start = date(requested_year, 1, 1)
        end = None

        if requested_year < today.year:
            end = date(requested_year, 12, 31)
        else:
            end = date(today.year, today.month, 1) - timedelta(days=1)

        print(start, end)
        return DateRange(start, end)