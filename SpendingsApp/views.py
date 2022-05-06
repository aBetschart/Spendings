from turtle import rt
from django.http import HttpRequest
from django.shortcuts import render
from .models import Spending


def home(request: HttpRequest):
    spendings = Spending.objects.all()
    return render(request, 'home.html', {'spendings': spendings})
