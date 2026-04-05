from abc import ABC, abstractmethod

from SpendingsApp.src.date_range import DateRange


class MonthlyAverageDataGateway(ABC):
    @abstractmethod
    def get_spending_amount(self, date_range: DateRange, category_id) -> float:
        pass