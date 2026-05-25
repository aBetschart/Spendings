
from dataclasses import dataclass
from typing import Dict

from SpendingsApp.finance.category_data import CategoryData
from SpendingsApp.request_data_preparation.category_converter import CategoryConverter

@dataclass(frozen=True)
class MonthlyAverageRequestData:
    year: int
    category: CategoryData


class MonthlyAverageDataPreparer:

    def __init__(self, category_converter: CategoryConverter):
        self._category_converter = category_converter


    def extract_average_data(self, request_data: Dict[str, any]) -> MonthlyAverageRequestData:
        year = self._extract_year(request_data)
        category = self._extract_category(request_data)
        return MonthlyAverageRequestData(year=year, category=category)


    def _extract_year(self, request_data: Dict[str, any]) -> int:
        year = request_data.get("year")
        if year is None:
            raise ValueError("Missing required field: year")
        
        try:
            year = int(year)
            if year < 0:
                raise ValueError()
            return year
        except (ValueError, TypeError):
            raise ValueError("Invalid year format: expected an integer greater than or equal to 0.")
        
    def _extract_category(self, request_data: Dict[str, any]) -> CategoryData:
        category_request = request_data.get("category")
        if category_request is None:
            raise ValueError("Missing required field: category")
        
        return self._category_converter.convert_to_category(category_request)        
