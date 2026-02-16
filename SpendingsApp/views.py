from typing import Dict, List
from django.forms.models import model_to_dict
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, JsonResponse, QueryDict
from django.shortcuts import render, redirect
from .models import Category, Spending
from .forms import SpendingForm, CategoryForm, MonthlyOverviewForm, YearlyOverviewForm, MONTH_CHOICES
from .src.date_range import DateRange

import sys
import calendar
from datetime import datetime, date
from dataclasses import dataclass
from http import HTTPStatus

DEFAULT_RECENT_SPENDINGS_COUNT = 10
RECENT_SPENDINGS_MAX_COUNT = 100

def home(request: HttpRequest) -> HttpResponse:
    spending_form = SpendingForm()
    args = {
        'spendingForm': spending_form,
    }
    return render(request, 'home.html', args)

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

    data = { 'spendings': form_spendings_response(spendings) }
    return JsonResponse(data, status=HTTPStatus.OK)

def get_filtered_spendings(filter_params):
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
        category_ids = [int(c) for c in categories]
    except Exception:
        raise ValueError("Category ID(s) must be integers")
    
    return category_ids

def extract_amount_range(request_data: Dict[str, any]) -> AmountRange:
    min_amount = 0
    max_amount = sys.float_info.max

    if 'min_amount' in request_data:
        min_amount = parse_amount(request_data['min_amount'])
        
    if 'max_amount' in request_data:
        max_amount = parse_amount(request_data['max_amount'])

    return AmountRange(min=min_amount, max=max_amount)

def extract_description(request_data: Dict[str, any]) -> str:
    if 'description' not in request_data:
        return ""
    
    return request_data['description']

def parse_amount(amount_str: str) -> float:
    try:
        return float(amount_str)
    except ValueError:
        raise ValueError("Invalid amount format. Expected a number")

def form_spendings_response(spendings: List[Spending]) -> List[Dict[str, any]]:
    response_spendings: List[Dict[str, any]] = []
    for spending in spendings:
        spending_dict = model_to_dict(spending)
        spending_dict['category'] = model_to_dict(spending.category)
        spending_dict['entryDate'] = spending.entryDate
        response_spendings.append(spending_dict)
    return response_spendings


def spending_get_recent_api(request: HttpRequest):
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


def spending_submit_api(request: HttpRequest) -> HttpResponse:
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
    try:
        id = int(category)
    except:
        name = category
        category = Category.objects.get(name=name)
        id = category.pk
    
    return id


def save_new_spending(data: Dict[str, any]):
    spendingDate = data['spendingDate']
    description = data['description']
    amount = data['amount']
    category = data['category']
    newSpending = Spending(spendingDate=spendingDate, description=description, amount=amount, category=category)
    newSpending.save()


def spending_delete_api(request: HttpRequest, id: int) -> HttpResponse:
    if request.method != 'POST':
        return HttpResponseNotAllowed(permitted_methods=['POST'])
    
    try:
        spending = Spending.objects.get(pk=id)
    except Spending.DoesNotExist:
        return JsonResponse({"errors": "Spending not found"}, status=HTTPStatus.NOT_FOUND)

    spending.delete()
    return JsonResponse({"message": "Spending deleted"}, status=HTTPStatus.OK)


def spending_edit(request: HttpRequest, id: int):
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


def spending_edit_api(request: HttpRequest, id: int) -> HttpResponse:
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


def category_edit_api(request: HttpRequest, id: int) -> HttpResponse:
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


def category_delete_api(request: HttpRequest, id: int) -> HttpResponse:
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


def category_edit(request: HttpRequest, id: int):
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


def extract_month_of_year(month_form: MonthlyOverviewForm) -> datetime:
    month_name = str(month_form.cleaned_data['month'])
    month = month_name_to_number(month_name)
    year = int(month_form.cleaned_data['year'])
    return datetime(day=1, month=month, year=year)


def month_name_to_number(monthName: str) -> int:
    cleanMonthName = monthName[0].upper() + monthName[1:].lower()
    return list(calendar.month_name).index(cleanMonthName)


def get_spendings_of_month(month: datetime) -> List[Spending]:
    start = get_first_day_of_month(month)
    end = get_last_day_of_month(month)
    order = '-spendingDate'
    return Spending.objects.filter(spendingDate__gte=start, spendingDate__lte=end).order_by(order)


def get_first_day_of_month(month: datetime) -> datetime:
    return datetime(year=month.year, month=month.month, day=1)


def get_last_day_of_month(month: datetime) -> datetime:
    lastDay = calendar.monthrange(month.year, month.month)[1]
    return datetime(year=month.year, month=month.month, day=lastDay)


def calculate_total(spendings: List[Spending]) -> float:
    sum = 0
    for spending in spendings:
        sum += spending.amount
    return sum


class YearlyCategorizedSpending():
    year: int
    category_name: str
    monthly_totals: dict[int, float]
    yearly_total: float

    def __init__(self) -> None:
        self.monthly_totals = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
            7: 0,
            8: 0,
            9: 0,
            10: 0,
            11: 0,
            12: 0,
        }


def yearly_overview(request: HttpRequest):
    year = datetime.now().year
    initial = { 'year': year }
    year_form = YearlyOverviewForm(initial=initial)

    if request.method == "POST":
        filled_form = YearlyOverviewForm(data=request.POST)
        if not filled_form.is_valid():
            return HttpResponseBadRequest("Invalid form request")
        
        year_form = filled_form
        year = int(year_form.cleaned_data['year'])
    
    categorized_spendings = get_categorized_spendings(year)
    yearly_total = calculate_yearly_total(categorized_spendings)

    args = {
        'year_form': year_form,
        'categorized_spendings': categorized_spendings,
        'yearly_total': yearly_total
    }
    return render(request, "year.html", args)


def get_categorized_spendings(year: int) -> List[YearlyCategorizedSpending]:
    categorized_spendings: List[YearlyCategorizedSpending] = []
    categories = Category.objects.order_by('name')
    for category in categories:
        yearlySpending = get_yearly_spending(year, category)        
        categorized_spendings.append(yearlySpending)

    return categorized_spendings


def get_yearly_spending(year: int, category: Category) -> YearlyCategorizedSpending:
    yearly_spending = YearlyCategorizedSpending()
    yearly_spending.year = year
    yearly_spending.category_name = str(category.name)

    for month in range(1, 13):
        spendings = get_monthly_spendings_from_category(category, month, year)
        yearly_spending.monthly_totals[month] = calculate_total(spendings)

    yearly_total = calc_yearly_total_of_category(yearly_spending)
    yearly_spending.yearly_total = yearly_total
    return yearly_spending


def get_monthly_spendings_from_category(category: Category, month: int, year: int) -> List[Spending]:
    month_of_year = datetime(day=1, month=month, year=year)
    first = get_first_day_of_month(month_of_year)
    last = get_last_day_of_month(month_of_year)
    return Spending.objects.filter(spendingDate__gte=first, spendingDate__lte=last, category=category)


def calc_yearly_total_of_category(yearly_spending: YearlyCategorizedSpending) -> float:
    yearly_total = 0
    for month in range(1, 13):
        yearly_total += yearly_spending.monthly_totals[month]
    return yearly_total


def calculate_yearly_total(categorized_spendings: List[YearlyCategorizedSpending]) -> float:
    yearly_total = 0
    for categorized_spending in categorized_spendings:
        yearly_total += categorized_spending.yearly_total
    return yearly_total

    