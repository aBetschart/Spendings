from django.http import HttpRequest
from django.shortcuts import render, redirect
from .models import Category, Spending
from .forms import SpendingForm, NewCategoryForm, MonthlySpendingOverview, MONTH_CHOICES

import calendar
from datetime import datetime

NUMBER_OF_RECENT_SPENDINGS = 10

def home(request: HttpRequest):
    spendingForm = SpendingForm()
    order = '-spendingDate'
    recentSpendings = Spending.objects.order_by(order)[:NUMBER_OF_RECENT_SPENDINGS]
    
    args = {
        'spendingForm': spendingForm,
        'spendings': recentSpendings,
    }
    return render(request, 'home.html', args)

def spending_submit(request: HttpRequest):
    if request.method == 'POST':
        newSpending = SpendingForm(data=request.POST)
        if newSpending.is_valid():
            newSpending.save()
    return redirect('home')

def spending_edit(request: HttpRequest, id: int):
    spending = Spending.objects.get(id=id)
    if request.method == 'POST':
        print(request.POST)
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

def monthly_overview(request: HttpRequest):
    month = datetime.now().month
    year = datetime.now().year
    monthIndex = month - 1
    initial = {
        'month': MONTH_CHOICES[monthIndex][0],
        'year': year
    }
    monthForm = MonthlySpendingOverview(initial=initial)
    monthlySpendings = []

    if request.method == 'POST':
        filledForm = MonthlySpendingOverview(data=request.POST)
        if not filledForm.is_valid():
            raise Exception("Month form was invalid")
        
        monthForm = filledForm
        monthName = str(monthForm.cleaned_data['month'])
        month = getMonthNumber(monthName)
        year = int(monthForm.cleaned_data['year'])
    
    monthlySpendings = getMonthlySpendings(month, year)
    args = {
        'monthForm': monthForm,
        'monthlySpendings': monthlySpendings,
    }
    return render(request, 'month.html', args)

def getMonthNumber(monthName: str) -> int:
    cleanMonthName = monthName[0].upper() + monthName[1:].lower()
    return list(calendar.month_name).index(cleanMonthName)

def getMonthlySpendings(month: int, year: int):
    start = getFirstDayOfMonth(month, year)
    end = getLastDayOfMonth(month, year)
    return Spending.objects.filter(spendingDate__gte=start, spendingDate__lte=end)

def getFirstDayOfMonth(month: int, year: int) -> datetime:
    return datetime(year=year, month=month, day=1)

def getLastDayOfMonth(month: int, year: int) -> datetime:
    lastDay = calendar.monthrange(year, month)[1]
    return datetime(year=year, month=month, day=lastDay)

def categories_edit(request: HttpRequest):
    if request.method == 'POST':
        filledForm = NewCategoryForm(data=request.POST)
        if filledForm.is_valid():
            newCategory = filledForm
            newCategory.save()

    categoryForm = NewCategoryForm()
    categories = Category.objects.order_by('name')
    args = {
        'categoryForm': categoryForm,
        'categories': categories,
    }
    return render(request, 'categories.html', args)

def category_delete(request: HttpRequest, id: int):
    category = Category.objects.get(id=id)
    category.delete()
    categoryForm = NewCategoryForm()
    categories = Category.objects.order_by('name')
    args = {
        'categoryForm': categoryForm,
        'categories': categories,
    }
    return render(request, 'categories.html', args)
