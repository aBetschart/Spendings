
from SpendingsApp.finance.category_data import CategoryData
from SpendingsApp.finance.monthly_average.monthly_average_data_gateway import MonthlyAverageDataGateway
from SpendingsApp.models import Spending
from SpendingsApp.src.date_range import DateRange


class MonthlyAverageDatabaseGateway(MonthlyAverageDataGateway):
    
    def get_spending_amount(self, date_range: DateRange, category: CategoryData) -> float:
        spendings = Spending.objects.filter(date__range=(date_range.start, date_range.end), category_id=category.id)
        return sum(spending.amount for spending in spendings)