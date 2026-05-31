

from datetime import date
import sys
from typing import List

from SpendingsApp.utils.date_range import DateRange

from .spending_filter_data import AmountRange, SpendingFilterData
from .spending_filter_request_data import SpendingFilterRequestData


class SpendingFilterExtractor:

    def extract_filter_data(self, request_data: SpendingFilterRequestData) -> SpendingFilterData: 
        if request_data.start_date is None:
            raise ValueError("Start date is required")

        if request_data.end_date is None:
            raise ValueError("End date is required")
        
        date_range = self._extract_date_range(request_data)
        category_ids = self._extract_category_ids(request_data)
        amount_range = self._extract_amount_range(request_data)
        description = self._extract_description(request_data)
        
        return SpendingFilterData(
            date_range=date_range,
            category_ids=category_ids,
            amount_range=amount_range,
            description=description
        )
    
    
    def _extract_date_range(self, request_data: SpendingFilterRequestData) -> DateRange:
        start_date = date.fromisoformat(request_data.start_date)
        end_date = date.fromisoformat(request_data.end_date)
        return DateRange(start=start_date, end=end_date)
    

    def _extract_category_ids(self, request_data: SpendingFilterRequestData) -> List[int]:
        category_ids_input = request_data.category_ids
        if category_ids_input is None:
            return []

        try:
            return [int(raw_id) for raw_id in category_ids_input]
        except ValueError as e:
            raise ValueError(f"Can not convert category IDs: {e}")
        

    def _extract_amount_range(self, request_data: SpendingFilterRequestData) -> AmountRange:
        min_amount = 0
        max_amount = sys.float_info.max

        request_min = request_data.min_amount
        request_max = request_data.max_amount

        if request_min == None and request_max == None:
            return None

        if request_data.min_amount is not None:
            try:
                min_amount = float(request_data.min_amount)
            except ValueError as e:
                raise ValueError(f"Could not convert amount: {e}")

        if request_data.max_amount is not None:
            try:
                max_amount = float(request_data.max_amount)
            except ValueError as e:
                raise ValueError(f"Could not convert amount: {e}")

        return AmountRange(min=min_amount, max=max_amount)
    

    def _extract_description(self, request_data: SpendingFilterRequestData) -> str:
        return request_data.description