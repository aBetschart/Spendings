from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect
from .models import Category, Spending
from .forms import SpendingForm, CategoryForm, MonthlyOverviewForm, YearlyOverviewForm, MONTH_CHOICES

import calendar
from datetime import datetime

DEFAULT_RECENT_SPENDINGS_COUNT = 10

def home(request: HttpRequest):
    spendingForm = SpendingForm()
    recentSpendings = get_recent_spendings(DEFAULT_RECENT_SPENDINGS_COUNT)

    args = {
        'spendingForm': spendingForm,
        'spendings': recentSpendings,
    }
    return render(request, 'home.html', args)

def get_recent_spendings(numberOfSpendings: int):
    order = '-entryDate'
    return Spending.objects.order_by(order)[:numberOfSpendings]

def spending_submit(request: HttpRequest):
    if request.method == 'POST':
        newSpending = SpendingForm(data=request.POST)
        if newSpending.is_valid():
            newSpending.save()
    return redirect('home')

def spending_submit_api(request: HttpRequest):
    data = {}
    status = 200

    if request.method == 'POST':
        postData = request.POST.dict()
        id = convert_to_category_id(postData['category'])
        postData['category'] = id

        form = SpendingForm(data=postData)
        if form.is_valid():
            save_new_spending(form.cleaned_data)
            data["message"] = "Spending entered"
        else:
            data["errors"] = form.errors
            status = 400

    return JsonResponse(data, status=status)

def convert_to_category_id(category):
    try:
        id = int(category)
    except:
        name = category
        category = Category.objects.get(name=name)
        id = category.pk
    
    return id

def save_new_spending(data: dict[str, any]):
    spendingDate = data['spendingDate']
    description = data['description']
    amount = data['amount']
    category = data['category']
    newSpending = Spending(spendingDate=spendingDate, description=description, amount=amount, category=category)
    newSpending.save()


def spending_get_recent_api(request: HttpRequest):
    data = {}
    status = 200

    if request.method == 'GET':
        queryData = request.GET
        try:
            spendingsCount = int(queryData['numberOfSpendings'])
        except:
            spendingsCount = DEFAULT_RECENT_SPENDINGS_COUNT
        
        spendings = get_recent_spendings(spendingsCount)
        data['spendings'] = form_spendings_response(spendings)
    else:
        data = {'message': 'Only GET here'}
        status = 400

    return JsonResponse(data, status=status)

def form_spendings_response(spendings):
    spendingResponse = []
    for spending in spendings:
        spendingDict = spendingToDict(spending)
        spendingResponse.append(spendingDict)
    return spendingResponse

def spendingToDict(spending: Spending) -> dict[str, any]:
    return {
        'id': spending.id,
        'spendingDate': spending.spendingDate,
        'description': spending.description,
        'amount': spending.amount,
        'category': {'id': spending.category.pk, 'name': spending.category.name},
    }

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

def monthly_overview(request: HttpRequest):
    month_of_year = datetime.now()
    month_form = setup_month_form(month_of_year)

    if request.method == 'POST':
        filled_form = MonthlyOverviewForm(data=request.POST)
        if not filled_form.is_valid():
            return HttpResponseBadRequest("Invalid form request")
        
        month_form = filled_form
        month_of_year = extract_month_of_year(month_form)
    
    monthly_spendings = get_spendings_of_month(month_of_year)
    monthlyTotal = calculate_total(monthly_spendings)
    args = {
        'monthForm': month_form,
        'monthlySpendings': monthly_spendings,
        'total': monthlyTotal,
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

def get_spendings_of_month(month: datetime):
    start = get_first_day_of_month(month)
    end = get_last_day_of_month(month)
    order = '-spendingDate'
    return Spending.objects.filter(spendingDate__gte=start, spendingDate__lte=end).order_by(order)

def get_first_day_of_month(month: datetime) -> datetime:
    return datetime(year=month.year, month=month.month, day=1)

def get_last_day_of_month(month: datetime) -> datetime:
    lastDay = calendar.monthrange(month.year, month.month)[1]
    return datetime(year=month.year, month=month.month, day=lastDay)

def calculate_total(spendings) -> float:
    sum = 0
    for spending in spendings:
        sum += spending.amount
    return sum

class YearlyCategorizedSpending():
    year: int
    category: str
    monthlyTotals: dict[int, float]
    yearlyTotalOfCategory: float

    def __init__(self) -> None:
        self.monthlyTotals = {
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
    yearForm = YearlyOverviewForm(initial=initial)

    if request.method == "POST":
        filledForm = YearlyOverviewForm(data=request.POST)
        if not filledForm.is_valid():
            return HttpResponseBadRequest("Invalid form request")
        
        yearForm = filledForm
        year = int(yearForm.cleaned_data['year'])
    
    categorized_spendings = get_categorized_spendings(year)
    yearlyTotal = calculate_yearly_total(categorized_spendings)

    args = {
        'yearForm': yearForm,
        'categorizedSpendings': categorized_spendings,
        'yearlyTotal': yearlyTotal
    }
    return render(request, "year.html", args)

def get_categorized_spendings(year: int):
    categorizedSpendings = []
    categories = Category.objects.order_by('name')
    for category in categories:
        yearlySpending = get_yearly_spending(year, category)        
        categorizedSpendings.append(yearlySpending)

    return categorizedSpendings

def get_yearly_spending(year: int, category: Category):
    yearlySpending = YearlyCategorizedSpending()
    yearlySpending.year = year
    yearlySpending.category = str(category.name)

    for month in range(1, 13):
        spendings = get_monthly_spendings_from_category(category, month, year)
        yearlySpending.monthlyTotals[month] = calculate_total(spendings)

    yearly_total = calc_yearly_total_of_category(yearlySpending)
    yearlySpending.yearlyTotalOfCategory = yearly_total
    return yearlySpending

def get_monthly_spendings_from_category(category: Category, month: int, year: int):
    month_of_year = datetime(day=1, month=month, year=year)
    first = get_first_day_of_month(month_of_year)
    last = get_last_day_of_month(month_of_year)
    return Spending.objects.filter(spendingDate__gte=first, spendingDate__lte=last, category=category)

def calc_yearly_total_of_category(yearly_spending):
    yearly_total = 0
    for month in range(1, 13):
        yearly_total += yearly_spending.monthlyTotals[month]
    return yearly_total

def calculate_yearly_total(categorizedSpendings):
    yearlyTotal = 0
    for categorizedSpending in categorizedSpendings:
        yearlyTotal += categorizedSpending.yearlyTotalOfCategory
    return yearlyTotal

    