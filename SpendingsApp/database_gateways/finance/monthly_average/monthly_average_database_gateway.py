
from django.contrib.auth import get_user_model

from SpendingsApp.finance.category_data import CategoryData
from SpendingsApp.finance.monthly_average.monthly_average_data_gateway import MonthlyAverageDataGateway
from SpendingsApp.finance.user_data import UserData
from SpendingsApp.models import Category, Spending
from SpendingsApp.utils.date_range import DateRange

User = get_user_model()


class MonthlyAverageDatabaseGateway(MonthlyAverageDataGateway):
    
    def get_spending_amount(self, date_range: DateRange, category: CategoryData, user: UserData) -> float:
        user = User.objects.get(id=user.id)
        category = Category.objects.get(id=category.id, user=user)
        spending_date_range = (date_range.start, date_range.end)
        spendings = Spending.objects.filter(spendingDate__range=spending_date_range, category=category, user=user)
        return sum(spending.amount for spending in spendings)