
from typing import Dict, List
from http import HTTPStatus

from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.generic import View
from django.shortcuts import render

from SpendingsApp.database_gateways.database_category_converter import DatabaseCategoryConverter
from SpendingsApp.database_gateways.filtering.spending_filter_database_gateway import SpendingFilterDatabaseGateway
from SpendingsApp.forms import SpendingForm
from SpendingsApp.models import Spending
from SpendingsApp.request_data_preparation.get_recent_spending.spendings_count_preparer import SpendingsCountPreparer
from SpendingsApp.request_data_preparation.spending_filtering.spending_filter_extractor import SpendingFilterExtractor
from SpendingsApp.request_data_preparation.spending_filtering.spending_filter_request_data import SpendingFilterRequestData

from .util import get_spending_from_id, convert_spending_to_dict, convert_spendings_to_dict, calculate_total

# ------------------------------
# ---------- Views
# ------------------------------

class SpendingView(View):
    def get(self, request: HttpRequest, id: int) -> HttpResponse:
        try:
            spending = get_spending_from_id(id)
        except ValueError as error:
            return HttpResponseBadRequest(str(error))
        
        spending_form = SpendingForm(instance=spending)
        context = {'spendingForm': spending_form}
        return render(request, 'spending.html', context)
    

# ------------------------------
# ---------- API
# ------------------------------


class SpendingEditApi(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._category_converter = DatabaseCategoryConverter()

    def post(self, request: HttpRequest, id: int) -> HttpResponse:
        try:
            spending = get_spending_from_id(id)
        except ValueError as error:
            return HttpResponseBadRequest(str(error))
        
        post_data = request.POST.dict()
        if not 'category' in post_data:
            return HttpResponseBadRequest("Missing 'category' field in request data.")
        
        categord_id = self._get_category_id(post_data['category'])
        post_data['category'] = categord_id
        form = SpendingForm(data=post_data, instance=spending)

        if not form.is_valid():
            return HttpResponseBadRequest(str(form.errors))
        
        form.save()

        spending_dict = convert_spending_to_dict(spending)
        message = "Spending edited successfully."
        data = {
            "message": message,
            "spending": spending_dict
        }
        return JsonResponse(data, status=HTTPStatus.OK)

    def _get_category_id(self, category_input: any) -> int:
        category_data = self._category_converter.convert_to_category(category_input)
        return category_data.id
    


class SpendingGetApi(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._filter_extractor = SpendingFilterExtractor()
        self._database_gateway = SpendingFilterDatabaseGateway()

    def get(self, request: HttpRequest) -> HttpResponse:
        request_data = SpendingFilterRequestData(
            start_date=request.GET.get('start_date'),
            end_date=request.GET.get('end_date'),
            category_ids=request.GET.getlist('categories'),
            min_amount=request.GET.get('min_amount'),
            max_amount=request.GET.get('max_amount'),
            description=request.GET.get('description', "")
        )

        try:
            filter_data = self._filter_extractor.extract_filter_data(request_data)
        except ValueError as error:
            return HttpResponseBadRequest(str(error))
        
        spendings = self._database_gateway.get_filtered_spendings(filter_data)

        total = calculate_total(spendings)
        spendings_dicts = convert_spendings_to_dict(spendings)
        data = {"spendings": spendings_dicts, "total": total}
        return JsonResponse(data, status=HTTPStatus.OK)
    


class SpendingGetRecentApi(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._preparer = SpendingsCountPreparer()

    def get(self, request: HttpRequest) -> HttpResponse:
        spendings_count = self._preparer.extract_spendings_count(request.GET)
        spendings = self._get_recent_spendings(spendings_count)
        spending_dicts = convert_spendings_to_dict(spendings)
        data = { 'spendings': spending_dicts }
        return JsonResponse(data, status=HTTPStatus.OK)
    
    def _get_recent_spendings(self, spendings_count: int) -> List[Spending]:
        order = '-entryDate'
        return Spending.objects.order_by(order)[:spendings_count]    
    


class SpendingPostApi(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._category_converter = DatabaseCategoryConverter()

    def post(self, request: HttpRequest) -> HttpResponse:
        post_data = request.POST.dict()
        form = self._convert_to_form(post_data)

        if not form.is_valid():
            return HttpResponseBadRequest(str(form.errors))
        
        new_spending = form.save()

        spending_dict = convert_spending_to_dict(new_spending)
        data = { "message": "Spending submitted successfully.", "spending": spending_dict }
        return JsonResponse(data, status=HTTPStatus.OK)
    
    def _convert_to_form(self, post_data: Dict[str, any]) -> SpendingForm:
        posted_category = post_data.get('category')
        category = self._category_converter.convert_to_category(posted_category)
        post_data['category'] = category.id
        return SpendingForm(data=post_data)
    


class SpendingDeleteApi(View):
    def post(self, request: HttpRequest, id: int) -> HttpResponse:
        try:
            spending = get_spending_from_id(id)
        except ValueError as error:
            return HttpResponseBadRequest(str(error))

        spending.delete()
        
        message = f"Spending with ID {id} deleted successfully."
        return JsonResponse({"message": message}, status=HTTPStatus.OK)    
