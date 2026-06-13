from abc import ABC, abstractmethod

from SpendingsApp.finance.category_data import CategoryData
from SpendingsApp.finance.user_data import UserData
from SpendingsApp.utils.date_range import DateRange


class MonthlyAverageDataGateway(ABC):

    @abstractmethod
    def get_spending_amount(self, date_range: DateRange, category: CategoryData, user: UserData) -> float:
        pass