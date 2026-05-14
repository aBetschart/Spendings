

from datetime import date

from SpendingsApp.src.date_range import DateRange

from .spending_filter_data import AmountRange, SpendingFilterData
from .spending_filter_request_data import SpendingFilterRequestData


class SpendingFilterExtractor:

    def extract_filter_data(self, request_data: SpendingFilterRequestData) -> SpendingFilterData: 
        if request_data.start_date is None:
            raise ValueError("Start date is required")

        if request_data.end_date is None:
            raise ValueError("End date is required")
        
        date_range = self._extract_date_range(request_data)

        
        category_ids = [1, 2, 3]
        amount_range = AmountRange(min=10.0, max=100.0)
        description = "Test description"
        filter_data = SpendingFilterData(
            date_range=date_range,
            category_ids=category_ids,
            amount_range=amount_range,
            description=description
        )

        return filter_data
    
    def _extract_date_range(self, request_data: SpendingFilterRequestData) -> DateRange:
        start_date = date.fromisoformat(request_data.start_date)
        end_date = date.fromisoformat(request_data.end_date)
        return DateRange(start=start_date, end=end_date)
    