
from abc import ABC, abstractmethod

from SpendingsApp.finance.category_data import CategoryData

class CategoryConverter(ABC):

    @abstractmethod
    def convert_to_category(self, input: any) -> CategoryData:
        pass