from django.http import HttpRequest, HttpResponseNotFound
from django.shortcuts import render
from .models import Category, Spending
from .forms import EnterSpendingForm, NewCategoryForm


def home(request: HttpRequest):
    spendingForm = EnterSpendingForm()
    categoryForm = NewCategoryForm()
    if request.method == 'POST':
        if 'submit-spending' in request.POST:
            filledForm = EnterSpendingForm(data=request.POST)
            if filledForm.is_valid():
                filledForm.save()
            else:
                print(filledForm.errors)
        elif 'submit-new-category' in request.POST:
            filledForm = NewCategoryForm(data=request.POST)
            if filledForm.is_valid():
                filledForm.save()
            else:
                print(filledForm.errors)
        else:
            return HttpResponseNotFound("Invalid post request")


    spendings = Spending.objects.all()
    categories = Category.objects.all()

    args = {
        'spendings': spendings,
        'spendingForm': spendingForm,
        'categoryForm': categoryForm,
        'categories': categories
    }
    return render(request, 'home.html', args)
