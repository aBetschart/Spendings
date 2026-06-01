
from dataclasses import asdict
from http import HTTPStatus

from django.http import HttpRequest, HttpResponseBadRequest, HttpResponseNotAllowed, JsonResponse

from SpendingsApp.database_gateways.database_category_converter import DatabaseCategoryConverter
from SpendingsApp.request_data_preparation.monthly_average.monthly_average_data_preparer import MonthlyAverageDataPreparer




from .database_gateways.finance.monthly_average.monthly_average_database_gateway import MonthlyAverageDatabaseGateway
from .finance.monthly_average.monthly_average_calculator import MonthlyAverageCalculator


# ------------------------------------------------------
# ------------------------- OTHER  ---------------------
# ------------------------------------------------------

def monthly_average(request: HttpRequest):
    if request.method != 'GET':
        return HttpResponseNotAllowed(permitted_methods=['GET'])

    database_category_converter = DatabaseCategoryConverter()
    request_data_preparer = MonthlyAverageDataPreparer(database_category_converter)

    request_data = {
        'year': request.GET.get('year'),
        'category': request.GET.get('category')
    }
    try:
        average_request_data = request_data_preparer.extract_average_data(request_data)
    except ValueError as e:
        return HttpResponseBadRequest(str(e))


    database_gateway = MonthlyAverageDatabaseGateway()
    average_calculator = MonthlyAverageCalculator(database_gateway)

    year = average_request_data.year
    category = average_request_data.category
    average = average_calculator.calculate_monthly_average(year, category)
    
    data = {
        'average': average,
        'year': year,
        'category': asdict(category),
    }
    return JsonResponse(data, status=HTTPStatus.OK)
    