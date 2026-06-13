
from datetime import date, timedelta

from SpendingsApp.finance.category_data import CategoryData
from SpendingsApp.finance.user_data import UserData
from SpendingsApp.utils.date_range import DateRange
from .monthly_average_data_gateway import MonthlyAverageDataGateway


class MonthlyAverageCalculator:
    def __init__(self, data_gateway: MonthlyAverageDataGateway):
        self._data_gateway = data_gateway

    def calculate_monthly_average(self, year: int, category: CategoryData, user: UserData) -> float:
        if year < 0:
            raise ValueError(f"Year cannot be negative but was '{year}'.")

        if not self._average_possible(year):
            return 0

        date_range = self._calc_date_range(year)
        amount = self._data_gateway.get_spending_amount(date_range, category, user)
        months_count = self._get_months_count(date_range)
        return amount / months_count
    
    def _average_possible(self, requested_year: int) -> bool:
        today = date.today()
        if requested_year > today.year:
            return False
        
        if requested_year == today.year:
            if today.month == 1:
                return False
            
        return True

    def _calc_date_range(self, requested_year: int) -> DateRange:
        today = date.today()
        start = date(requested_year, 1, 1)
        end = None

        if requested_year < today.year:
            end = date(requested_year, 12, 31)
        else:
            end = date(today.year, today.month, 1) - timedelta(days=1)

        return DateRange(start, end)
    
    def _get_months_count(self, date_range: DateRange) -> int:
        start = date_range.start
        end = date_range.end
        return end.month - start.month + 1
    