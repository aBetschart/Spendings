
from datetime import datetime
from dataclasses import asdict
from http import HTTPStatus
from typing import Dict, List

from django.forms.models import model_to_dict
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render, redirect

from SpendingsApp.database_gateways.database_category_converter import DatabaseCategoryConverter
from SpendingsApp.database_gateways.filtering.spending_filter_database_gateway import SpendingFilterDatabaseGateway
from SpendingsApp.request_data_preparation.get_recent_spending.spendings_count_preparer import SpendingsCountPreparer
from SpendingsApp.request_data_preparation.monthly_average.monthly_average_data_preparer import MonthlyAverageDataPreparer
from SpendingsApp.request_data_preparation.spending_filtering.spending_filter_extractor import SpendingFilterExtractor
from SpendingsApp.request_data_preparation.spending_filtering.spending_filter_request_data import SpendingFilterRequestData
from .models import Category, Spending
from .forms import SpendingForm, CategoryForm, MonthlyOverviewForm, YearlyOverviewForm, MONTH_CHOICES

from .database_gateways.finance.monthly_average.monthly_average_database_gateway import MonthlyAverageDatabaseGateway
from .finance.monthly_average.monthly_average_calculator import MonthlyAverageCalculator


# ------------------------------------------------------
# ------------------------- SPENDING  ------------------
# ------------------------------------------------------


def spending_get(request: HttpRequest) -> HttpResponse:
    if not request.method == 'GET':
        return HttpResponseNotAllowed(permitted_methods=['GET'])

    request_data = SpendingFilterRequestData(
        start_date=request.GET.get('start_date'),
        end_date=request.GET.get('end_date'),
        category_ids=request.GET.getlist('categories'),
        min_amount=request.GET.get('min_amount'),
        max_amount=request.GET.get('max_amount'),
        description=request.GET.get('description', "")
    )

    filter_extractor = SpendingFilterExtractor()
    try:
        filter_data = filter_extractor.extract_filter_data(request_data)
    except ValueError as e:
        return JsonResponse({"errors": str(e)}, status=HTTPStatus.BAD_REQUEST)
    
    spending_filter_gateway = SpendingFilterDatabaseGateway()
    spendings = spending_filter_gateway.get_filtered_spendings(filter_data)

    total = calculate_total(spendings)
    spendings_response = form_spendings_response(spendings)
    data = { 'spendings': spendings_response, 'total': total }
    return JsonResponse(data, status=HTTPStatus.OK)


def calculate_total(spendings: List[Spending]) -> float:
    sum = 0
    for spending in spendings:
        sum += spending.amount
    return sum


def form_spendings_response(spendings: List[Spending]) -> List[Dict[str, any]]:
    response_spendings: List[Dict[str, any]] = []
    for spending in spendings:
        spending_dict = model_to_dict(spending)
        spending_dict['category'] = model_to_dict(spending.category)
        spending_dict['entryDate'] = spending.entryDate
        response_spendings.append(spending_dict)
    return response_spendings


def spending_get_recent(request: HttpRequest):
    preparer = SpendingsCountPreparer()
    spendings_count = preparer.extract_spendings_count(request.POST)
    spendings = get_recent_spendings(spendings_count)
    data = { 'spendings': form_spendings_response(spendings) }
    return JsonResponse(data, status=HTTPStatus.OK)


def get_recent_spendings(numberOfSpendings: int) -> List[Spending]:
    order = '-entryDate'
    return Spending.objects.order_by(order)[:numberOfSpendings]


def spending_submit(request: HttpRequest) -> HttpResponse:
    if request.method != 'POST':
        return HttpResponseNotAllowed(permitted_methods=['POST'])

    post_data = request.POST.dict()
    form = convert_submit_post_data_to_form(post_data)

    if not form.is_valid():
        data = { "errors": form.errors }
        return JsonResponse(data=data, status=HTTPStatus.BAD_REQUEST)
    
    save_new_spending(form.cleaned_data)
    data = { "message": "Spending submitted" }
    return JsonResponse(data, status=HTTPStatus.OK)


def convert_submit_post_data_to_form(post_data: Dict[str, any]) -> SpendingForm:
    id = convert_to_category_id(post_data['category'])
    post_data['category'] = id
    return SpendingForm(data=post_data)


def convert_to_category_id(category: any) -> int:
    if Category.objects.filter(name__iexact=category).exists():
        category = Category.objects.get(name=category)
        return category.pk

    try:
        return int(category)
    except:
        raise ValueError(f"Invalid category '{category}'. Expected category name or ID")


def save_new_spending(data: Dict[str, any]):
    spendingDate = data['spendingDate']
    description = data['description']
    amount = data['amount']
    category = data['category']
    newSpending = Spending(spendingDate=spendingDate, description=description, amount=amount, category=category)
    newSpending.save()


def spending_delete(request: HttpRequest, id: int) -> HttpResponse:
    if request.method != 'POST':
        return HttpResponseNotAllowed(permitted_methods=['POST'])
    
    try:
        spending = Spending.objects.get(pk=id)
    except Spending.DoesNotExist:
        return JsonResponse({"errors": "Spending not found"}, status=HTTPStatus.NOT_FOUND)

    spending.delete()
    return JsonResponse({"message": "Spending deleted"}, status=HTTPStatus.OK)


def spending_view(request: HttpRequest, id: int) -> HttpResponse:
    spending = Spending.objects.get(id=id)
    if request.method == 'POST':
        editedSpending = SpendingForm(data=request.POST, instance=spending)
        if editedSpending.is_valid():
            if 'delete_spending' in request.POST:
                spending.delete()
                return redirect('home')
            else:
                return HttpResponseNotAllowed(permitted_methods=['POST with delete_spending field'])

    spending_form = SpendingForm(instance=spending)

    args = { 'spendingForm': spending_form }
    return render(request, 'spending.html', args)


def spending_edit(request: HttpRequest, id: int) -> HttpResponse:
    if request.method != "POST":
        return HttpResponseNotAllowed(permitted_methods=['POST'])

    post_data = request.POST.dict()

    try:
        spending = Spending.objects.get(pk=id)
    except Spending.DoesNotExist:
        return JsonResponse({"errors": "Spending not found"}, status=HTTPStatus.NOT_FOUND)

    if 'category' in post_data:
        post_data['category'] = convert_to_category_id(post_data['category'])

    edited_form = SpendingForm(data=post_data, instance=spending)
    if not edited_form.is_valid():
        return JsonResponse({"errors": edited_form.errors}, status=HTTPStatus.BAD_REQUEST)

    edited_form.save()

    spending_dict = model_to_dict(spending)
    spending_dict['category'] = model_to_dict(spending.category)
    spending_dict['entryDate'] = spending.entryDate

    return JsonResponse({"message": "Spending edited", "spending": spending_dict}, status=HTTPStatus.OK)




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
    