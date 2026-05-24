
from typing import List

from SpendingsApp.request_data_preparation.spending_filtering.spending_filter_data import SpendingFilterData
from SpendingsApp.models import Spending
from SpendingsApp.utils.date_range import DateRange


class SpendingFilterDatabaseGateway:
    
    def get_filtered_spendings(self, filter_data: SpendingFilterData) -> List[Spending]:
        date_range: DateRange = filter_data.date_range
        start_date = date_range.start
        end_date = date_range.end
        spendings = Spending.objects.filter(spendingDate__gte=start_date, spendingDate__lte=end_date)

        if filter_data.category_ids != []:
            spendings = spendings.filter(category__in=filter_data.category_ids)

        amount_range = filter_data.amount_range
        if amount_range is not None:
            spendings = spendings.filter(amount__gte=amount_range.min, amount__lte=amount_range.max)
        
        if filter_data.description != "":
            spendings = spendings.filter(description__icontains=filter_data.description)

        return spendings.order_by('-spendingDate')