"""Spendings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import django.contrib.auth.views

from django.contrib import admin
from django.urls import path

from SpendingsApp.forms import CustomAuthenticationForm
from SpendingsApp.views import pages, category, spending, api

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', django.contrib.auth.views.LoginView.as_view(template_name='login.html', form_class=CustomAuthenticationForm), name='login'),

    path('', pages.HomeView.as_view(), name='home'),
    path('filter/', pages.FilterView.as_view(), name='filter'),
    path('month/', pages.MonthView.as_view(), name='monthly_overview'),
    path('year/', pages.YearView.as_view(), name='yearly_overview'),
    
    path('spending/<int:id>', spending.SpendingView.as_view(), name='spending_view'),
    path('spending/get', spending.SpendingGetApi.as_view(), name='spending_get'),
    path('spending/get/recent', spending.SpendingGetRecentApi.as_view(), name='spending_get_recent'),
    path('spending/post', spending.SpendingPostApi.as_view(), name='spending_post'),
    path('spending/edit/<int:id>', spending.SpendingEditApi.as_view(), name='spending_edit'),
    path('spending/delete/<int:id>', spending.SpendingDeleteApi.as_view(), name='spending_delete'),

    path('categories', category.CategoryOverview.as_view(), name='categories'),
    path('category/<int:id>', category.CategoryEditView.as_view(), name='category_view'),
    path('category/get', category.CategoryGetApi.as_view(), name='category_get'),
    path('category/post', category.CategoryPostApi.as_view(), name='category_post'),
    path('category/edit/<int:id>', category.CategoryEditApi.as_view(), name='category_edit'),
    path('category/delete/<int:id>', category.CategoryDeleteApi.as_view(), name='category_delete'),

    path('average/monthly', api.MonthlyAverageApi.as_view(), name='monthly_average'),
]
