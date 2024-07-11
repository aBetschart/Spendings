from django.http import HttpRequest, HttpResponseNotFound
from django.shortcuts import render, redirect
from django import forms
from .models import Category, Spending
from .forms import EnterSpendingForm, NewCategoryForm, MonthlySpendingOverview

import calendar
from datetime import datetime

NUMBER_OF_RECENT_SPENDINGS = 10

def home(request: HttpRequest):
    spendingForm = EnterSpendingForm()
    order = '-spendingDate'
    recentSpendings = Spending.objects.order_by(order)[:NUMBER_OF_RECENT_SPENDINGS]
    
    args = {
        'spendingForm': spendingForm,
        'spendings': recentSpendings,
    }
    return render(request, 'home.html', args)

def spending_submit(request: HttpRequest):
    if request.method == 'POST':
        newSpending = EnterSpendingForm(data=request.POST)
        if newSpending.is_valid():
            newSpending.save()
    return redirect('home')

def monthly_overview(request: HttpRequest):
    monthlySpendings = []
    monthForm = MonthlySpendingOverview()
    if request.method == 'POST':
        filledForm = MonthlySpendingOverview(data=request.POST)
        if not filledForm.is_valid():
            raise Exception("Month form was invalid")
        
        monthForm = filledForm
        year = int(monthForm.cleaned_data['year'])
        monthName = str(monthForm.cleaned_data['month'])
        cleanMonthName = monthName[0].upper() + monthName[1:].lower()
        monthNumber = list(calendar.month_name).index(cleanMonthName)
        firstDay = 1
        lastDay = calendar.monthrange(year, monthNumber)[1]
        start = datetime(year=year, month=monthNumber, day=firstDay)
        end = datetime(year=year, month=monthNumber, day=lastDay)
        monthlySpendings = Spending.objects.filter(spendingDate__gte=start, spendingDate__lte=end)
    
    args = {
        'monthForm': monthForm,
        'monthlySpendings': monthlySpendings,
    }
    return render(request, 'month.html', args)

def edit_categories(request: HttpRequest):
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
