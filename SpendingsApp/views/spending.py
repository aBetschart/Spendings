
from http import HTTPStatus

from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.generic import View
from django.shortcuts import render

from SpendingsApp.database_gateways.database_category_converter import DatabaseCategoryConverter
from SpendingsApp.forms import SpendingForm

from .util import get_spending_from_id, convert_spending_to_dict

class SpendingView(View):
    def get(self, request: HttpRequest, id: int) -> HttpResponse:
        try:
            spending = get_spending_from_id(id)
        except ValueError as error:
            return HttpResponseBadRequest(str(error))
        
        spending_form = SpendingForm(instance=spending)
        context = {'spendingForm': spending_form}
        return render(request, 'spending.html', context)
    


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
