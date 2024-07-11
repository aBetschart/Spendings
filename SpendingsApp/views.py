from django.http import HttpRequest, HttpResponseNotFound
from django.shortcuts import render, redirect
from django import forms
from .models import Category, Spending
from .forms import EnterSpendingForm, NewCategoryForm, MonthlySpendingOverview

import calendar
from datetime import datetime

NUMBER_OF_RECENT_SPENDINGS = 25

def home(request: HttpRequest):
    selectedYear = datetime.now().year
    selectedMonth = datetime.now().month
    monthlySpendings = []

    if request.method == 'POST':
        filledForm = forms.Form(data=request.POST)
        if not filledForm.is_valid():
            print(filledForm.errors)
            return

        if 'submit-spending' in request.POST:
            filledForm = EnterSpendingForm(data=request.POST)
            filledForm.save()
        elif 'submit-new-category' in request.POST:
            filledForm = NewCategoryForm(data=request.POST)
            filledForm.save()
        elif 'request-month-overview' in request.POST:
            filledForm = MonthlySpendingOverview(data=request.POST)
            if filledForm.is_valid():
                pass
            year = int(filledForm.cleaned_data['year'])
            monthName = str(filledForm.cleaned_data['month'])
            cleanMonthName = monthName[0].upper() + monthName[1:].lower()
            monthNumber = list(calendar.month_name).index(cleanMonthName)
            firstDay = 1
            lastDay = calendar.monthrange(year, monthNumber)[1]
            start = datetime(year=year, month=monthNumber, day=firstDay)
            end = datetime(year=year, month=monthNumber, day=lastDay)
            monthlySpendings = Spending.objects.filter(spendingDate__gte=start, spendingDate__lte=end)
        else:
            return HttpResponseNotFound("Invalid post request")


    recentSpendings = Spending.objects.order_by('-spendingDate')[:NUMBER_OF_RECENT_SPENDINGS]
    categories = Category.objects.order_by('name')
    
    spendingForm = EnterSpendingForm()
    categoryForm = NewCategoryForm()
    monthForm = MonthlySpendingOverview()

    args = {
        'spendings': recentSpendings,
        'categories': categories,
        'spendingForm': spendingForm,
        'categoryForm': categoryForm,
        'monthForm': monthForm,
        'monthlySpendings': monthlySpendings,
    }
    return render(request, 'home.html', args)

def spending_submit(request: HttpRequest):
    if request.method == 'POST':
        newSpending = EnterSpendingForm(data=request.POST)
        if newSpending.is_valid():
            newSpending.save()
    return redirect('home')
