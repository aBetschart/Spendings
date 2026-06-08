

from dataclasses import asdict
from http import HTTPStatus

from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
from SpendingsApp.views.auth_views import AuthenticatedView

from SpendingsApp.database_gateways.database_category_converter import DatabaseCategoryConverter
from SpendingsApp.database_gateways.finance.monthly_average.monthly_average_database_gateway import MonthlyAverageDatabaseGateway
from SpendingsApp.finance.monthly_average.monthly_average_calculator import MonthlyAverageCalculator
from SpendingsApp.request_data_preparation.monthly_average.monthly_average_data_preparer import MonthlyAverageDataPreparer

# TODO: Multi-User support

class MonthlyAverageApi(AuthenticatedView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._category_converter = DatabaseCategoryConverter()
        self._data_preparer = MonthlyAverageDataPreparer(self._category_converter)
        self._database_gateway = MonthlyAverageDatabaseGateway()
        self._average_calculator = MonthlyAverageCalculator(self._database_gateway)

    def get(self, request: HttpRequest) -> HttpResponse:
        request_data = {
            'year': request.GET.get('year'),
            'category': request.GET.get('category')
        }
        try:
            average_request_data = self._data_preparer.extract_average_data(request_data)
        except ValueError as e:
            return HttpResponseBadRequest(str(e))

        year = average_request_data.year
        category = average_request_data.category
        average = self._average_calculator.calculate_monthly_average(year, category)
        
        data = {
            'average': average,
            'year': year,
            'category': asdict(category),
        }
        return JsonResponse(data, status=HTTPStatus.OK)