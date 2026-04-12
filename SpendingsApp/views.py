
import sys
from datetime import datetime, date
from dataclasses import dataclass, asdict
from http import HTTPStatus
from typing import Dict, List

from django.forms.models import model_to_dict
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, JsonResponse, QueryDict
from django.shortcuts import render, redirect
from .models import Category, Spending
from .forms import SpendingFilterForm, SpendingForm, CategoryForm, MonthlyOverviewForm, YearlyOverviewForm, MONTH_CHOICES

from .src.date_range import DateRange
from .database_gateways.category_converter import CategoryConverter
from .database_gateways.finance.monthly_average.monthly_average_database_gateway import MonthlyAverageDatabaseGateway
from .finance.category_data import CategoryData
from .finance.monthly_average.monthly_average_calculator import MonthlyAverageCalculator

DEFAULT_RECENT_SPENDINGS_COUNT = 10
RECENT_SPENDINGS_MAX_COUNT = 100

def home(request: HttpRequest) -> HttpResponse:
    if request.method != 'GET':
        return HttpResponseNotAllowed(permitted_methods=['GET'])

    data = { 'spendingForm': SpendingForm() }
    return render(request, 'home.html', data)

def filter(request: HttpRequest) -> HttpResponse:
    spending_filter_form = SpendingFilterForm()
    args = {
        'spendingFilterForm': spending_filter_form,
    }
    return render(request, 'filter.html', args)

# ------------------------------------------------------
# ------------------------- SPENDING  ------------------
# ------------------------------------------------------

@dataclass(frozen=True)
class AmountRange:
    min: float
    max: float

    def __post_init__(self) -> None:
        if self.min < 0 or self.max < 0:
            raise ValueError("Amount cannot be negative")
        if self.min > self.max:
            raise ValueError("min amount cannot be greater than max amount")

@dataclass(frozen=True)
class SpendingFilterParams():
    date_range: DateRange
    categories: List[int]
    amount_range: AmountRange
    description: str


def spending_get(request: HttpRequest) -> HttpResponse:
    if not request.method == 'GET':
        return HttpResponseNotAllowed(permitted_methods=['GET'])

    try:
        filter_params = extract_filter_params(request.GET)
    except ValueError as e:
        return JsonResponse({"errors": str(e)}, status=HTTPStatus.BAD_REQUEST)

    spendings = get_filtered_spendings(filter_params)

    total = calculate_total(spendings)
    spendings_response = form_spendings_response(spendings)
    data = { 'spendings': spendings_response, 'total': total }
    return JsonResponse(data, status=HTTPStatus.OK)

def get_filtered_spendings(filter_params: SpendingFilterParams) -> List[Spending]:
    date_range = filter_params.date_range
    start_date = date_range.start
    end_date = date_range.end
    spendings = Spending.objects.filter(spendingDate__gte=start_date, spendingDate__lte=end_date)

    if filter_params.categories != []:
        spendings = spendings.filter(category__in=filter_params.categories)

    amount_range = filter_params.amount_range
    spendings = spendings.filter(amount__gte=amount_range.min, amount__lte=amount_range.max)
    
    if filter_params.description != "":
        spendings = spendings.filter(description__icontains=filter_params.description)

    return spendings.order_by('-spendingDate')

def extract_filter_params(request_data: QueryDict) -> SpendingFilterParams:    
    date_range = extract_date_range(request_data.dict())
    categories = extract_categories(request_data)
    amount_range = extract_amount_range(request_data.dict())
    description = extract_description(request_data.dict())
    
    return SpendingFilterParams(date_range=date_range, categories=categories, amount_range=amount_range, description=description)

def extract_date_range(request_data: Dict[str, any]) -> DateRange:
    try:
        start_date_param = request_data['start_date']
        end_date_param = request_data['end_date']
    except KeyError:
        raise ValueError("Missing required parameters: start_date or/and end_date")

    try:
        start_date = date.fromisoformat(start_date_param)
        end_date = date.fromisoformat(end_date_param)
    except ValueError:
        raise ValueError("Invalid date format. Expected ISO format: YYYY-MM-DD")

    return DateRange(start=start_date, end=end_date)

def extract_categories(request_data: QueryDict) -> List[int]:
    if 'categories' not in request_data:
        return []
    
    categories = request_data.getlist('categories')
    try:
        category_ids = [convert_to_category_id(c) for c in categories]
    except Exception:
        raise ValueError("Category ID not found")
    
    return category_ids

def extract_amount_range(request_data: Dict[str, any]) -> AmountRange:
    min_amount = 0
    max_amount = sys.float_info.max

    if 'min_amount' in request_data:
        min_amount = parse_amount(request_data['min_amount'])
        
    if 'max_amount' in request_data:
        max_amount = parse_amount(request_data['max_amount'])

    return AmountRange(min=min_amount, max=max_amount)

def parse_amount(amount_str: str) -> float:
    try:
        return float(amount_str)
    except ValueError:
        raise ValueError("Invalid amount format. Expected a number")

def extract_description(request_data: Dict[str, any]) -> str:
    if 'description' not in request_data:
        return ""
    
    return request_data['description']

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
    spendings_count = extract_spendings_count(request.POST)
    spendings = get_recent_spendings(spendings_count)
    data = { 'spendings': form_spendings_response(spendings) }
    return JsonResponse(data, status=HTTPStatus.OK)

def extract_spendings_count(query_data):
    try:
        spendings_count = int(query_data['spendings_count'])
    except:
        spendings_count = DEFAULT_RECENT_SPENDINGS_COUNT

    if spendings_count < 1:
        return 1

    if spendings_count > RECENT_SPENDINGS_MAX_COUNT:
        return RECENT_SPENDINGS_MAX_COUNT

    return spendings_count

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


def spending_view(request: HttpRequest, id: int):
    spending = Spending.objects.get(id=id)
    if request.method == 'POST':
        editedSpending = SpendingForm(data=request.POST, instance=spending)
        if editedSpending.is_valid():
            if 'edit-spending' in request.POST:
                editedSpending.save()
            elif 'delete-spending' in request.POST:
                spending.delete()
                return redirect('home')

    spendingForm = SpendingForm(instance=spending)

    args = {
        'spendingForm': spendingForm
    }
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
# ------------------------- CATEGORY  ------------------
# ------------------------------------------------------

def category_post(request: HttpRequest) -> HttpResponse:
    if request.method != 'POST':
        return HttpResponseNotAllowed(permitted_methods=['POST'])
    
    filledForm = CategoryForm(data=request.POST)
    if not filledForm.is_valid():
        return JsonResponse({"errors": filledForm.errors}, status=HTTPStatus.BAD_REQUEST)

    newCategory = filledForm.save()
    category_dict = model_to_dict(newCategory)
    return JsonResponse({"message": "Category created", "category": category_dict}, status=HTTPStatus.OK)


def category_get(request: HttpRequest) -> HttpResponse:
    if request.method != 'GET':
        return HttpResponseNotAllowed(permitted_methods=['GET'])
    
    categories = Category.objects.order_by('name')
    categories_dicts = [model_to_dict(category) for category in categories]
    return JsonResponse({"categories": categories_dicts}, status=HTTPStatus.OK)


def category_edit(request: HttpRequest, id: int) -> HttpResponse:
    if request.method != 'POST':
        return HttpResponseNotAllowed(permitted_methods=['POST'])
    
    try:
        category = Category.objects.get(pk=id)
    except Category.DoesNotExist:
        return JsonResponse({"errors": "Category not found"}, status=HTTPStatus.NOT_FOUND)

    edited_form = CategoryForm(data=request.POST, instance=category)
    if not edited_form.is_valid():
        return JsonResponse({"errors": edited_form.errors}, status=HTTPStatus.BAD_REQUEST)

    edited_form.save()
    category_dict = model_to_dict(category)
    return JsonResponse({"message": "Category edited", "category": category_dict}, status=HTTPStatus.OK)


def category_delete(request: HttpRequest, id: int) -> HttpResponse:
    if request.method != 'POST':
        return HttpResponseNotAllowed(permitted_methods=['POST'])
    
    try:
        category = Category.objects.get(pk=id)
    except Category.DoesNotExist:
        return JsonResponse({"errors": "Category not found"}, status=HTTPStatus.NOT_FOUND)

    if is_category_used(category):
        message = "Category is used by existing spendings and cannot be deleted"
        return JsonResponse({"errors": message}, status=HTTPStatus.BAD_REQUEST)

    category.delete()
    return JsonResponse({"message": "Category deleted"}, status=HTTPStatus.OK)


def is_category_used(category: Category) -> bool:
    spendings = Spending.objects.filter(category=category)
    return spendings.exists()


def categories(request: HttpRequest):
    if request.method == 'POST':
        filledForm = CategoryForm(data=request.POST)
        if filledForm.is_valid():
            newCategory = filledForm
            newCategory.save()

    categoryForm = CategoryForm()
    categories = Category.objects.order_by('name')
    args = {
        'categoryForm': categoryForm,
        'categories': categories,
    }
    return render(request, 'categories.html', args)


def category_view(request: HttpRequest, id: int):
    category = Category.objects.get(pk=id)
    if request.method == 'POST':
        editedCategory = CategoryForm(data=request.POST, instance=category)
        if editedCategory.is_valid():
            if 'edit-category' in request.POST:
                editedCategory.save()
            elif 'delete-category' in request.POST:
                category.delete()
                return redirect('categories')
    
    categoryForm = CategoryForm(instance=category)
    args = {
        "categoryForm": categoryForm
    }
    return render(request, "category.html", args)


def category_delete(request: HttpRequest, id: int):
    category = Category.objects.get(id=id)
    category.delete()
    categoryForm = CategoryForm()
    categories = Category.objects.order_by('name')
    args = {
        'categoryForm': categoryForm,
        'categories': categories,
    }
    return render(request, 'categories.html', args)



# ------------------------------------------------------
# ------------------------- MONTH  ---------------------
# ------------------------------------------------------

def monthly_overview(request: HttpRequest):
    if request.method != 'GET':
        return HttpResponseNotAllowed(permitted_methods=['GET'])

    month_of_year = datetime.now()
    month_form = setup_month_form(month_of_year)
    
    args = {
        'monthForm': month_form,
    }
    return render(request, 'month.html', args)


def setup_month_form(month_of_year: datetime) -> MonthlyOverviewForm:
    monthIndex = month_of_year.month - 1
    initial = {
        'month': MONTH_CHOICES[monthIndex][0],
        'year': month_of_year.year
    }
    return MonthlyOverviewForm(initial=initial)


# ------------------------------------------------------
# ------------------------- YEAR  ----------------------
# ------------------------------------------------------

def yearly_overview(request: HttpRequest):
    if request.method != 'GET':
        return HttpResponseNotAllowed(permitted_methods=['GET'])

    year = datetime.now().year
    initial = { 'year': year }
    year_form = YearlyOverviewForm(initial=initial)

    data = { 'year_form': year_form }
    return render(request, "year.html", data)


# ------------------------------------------------------
# ------------------------- OTHER  ---------------------
# ------------------------------------------------------

@dataclass(frozen=True)
class MonthlyAverageRequestData:
    year: int
    category: CategoryData

def monthly_average(request: HttpRequest):
    if request.method != 'GET':
        return HttpResponseNotAllowed(permitted_methods=['GET'])

    query_data = request.GET.dict()
    print(query_data)
    try:
        request_data = extract_monthly_average_request_data(query_data)
    except ValueError as e:
        return HttpResponseBadRequest(str(e))

    database_gateway = MonthlyAverageDatabaseGateway()
    average_calculator = MonthlyAverageCalculator(database_gateway)

    category = request_data.category
    category_data = CategoryData(id=category.id, name=category.name)
    average = average_calculator.calculate_monthly_average(request_data.year, category_data)
    
    data = {
        'average': average,
        'category': asdict(category_data),
        'year': request_data.year,
    }
    return JsonResponse(data, status=HTTPStatus.OK)
    
def extract_monthly_average_request_data(query_data: Dict[str, any]) -> MonthlyAverageRequestData:
    if not 'year' in query_data:
        raise ValueError("Missing required parameter: year")
    
    try:
        year = int(query_data['year'])
    except ValueError:
        raise ValueError("Invalid year format. Expected a number")
    
    if not 'category' in query_data:
        raise ValueError("Missing required parameter: category")
    
    category_converter = CategoryConverter()
    queried_category = query_data['category']
    try:
        category = category_converter.convert_to_category(queried_category)
    except ValueError as e:
        raise ValueError(str(e))

    category_data = CategoryData(id=category.id, name=category.name)
    return MonthlyAverageRequestData(year=year, category=category_data)