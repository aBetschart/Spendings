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
from django.contrib import admin
from django.urls import path

from SpendingsApp import views_file
from SpendingsApp.views import pages, category, spending

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', pages.HomeView.as_view(), name='home'),
    path('filter/', pages.FilterView.as_view(), name='filter'),
    path('month/', pages.MonthView.as_view(), name='monthly_overview'),
    path('year/', pages.YearView.as_view(), name='yearly_overview'),

    
    path('spending/<int:id>', spending.SpendingView.as_view(), name='spending_view'),
    path('spending/get/', views_file.spending_get, name='spending_get'),
    path('spending/get/recent', views_file.spending_get_recent, name='spending_get_recent'),
    path('spending/submit/api', views_file.spending_submit, name='spending_submit_api'),
    path('spending/edit/<int:id>', spending.SpendingEditApi.as_view(), name='spending_edit'),
    path('spending/delete/api/<int:id>', views_file.spending_delete, name='spending_delete_api'),

    path('categories', category.CategoryOverview.as_view(), name='categories'),
    path('categories/edit/<int:id>', category.CategoryEditView.as_view(), name='category_edit'),

    path('category/post', category.CategoryPostApi.as_view(), name='category_post'),
    path('category/get', category.CategoryGetApi.as_view(), name='category_get'),
    path('category/edit/<int:id>', category.CategoryEditApi.as_view(), name='category_edit_api'),
    path('category/delete/<int:id>', category.CategoryDeleteApi.as_view(), name='category_delete'),

    path('average/monthly', views_file.monthly_average, name='monthly_average'),
]
