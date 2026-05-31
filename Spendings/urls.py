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
from SpendingsApp.views import pages

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', pages.HomeView.as_view(), name='home'),
    path('filter/', pages.FilterView.as_view(), name='filter'),
    path('month/', pages.MonthView.as_view(), name='monthly_overview'),
    path('year/', pages.YearView.as_view(), name='yearly_overview'),

    
    path('spending/submit/api', views_file.spending_submit, name='spending_submit_api'),
    path('spending/get/', views_file.spending_get, name='spending_get'),
    path('spending/get/recent', views_file.spending_get_recent, name='spending_get_recent'),
    path('spending/delete/api/<int:id>', views_file.spending_delete, name='spending_delete_api'),
    path('spending/edit/<int:id>', views_file.spending_view, name='spending_edit'),
    path('spending/edit/api/<int:id>', views_file.spending_edit, name='spending_edit_api'),

    path('categories', views_file.categories, name='categories'),
    path('categories/edit/<int:id>', views_file.category_view, name='category_edit'),

    path('category/post', views_file.category_post, name='category_post'),
    path('category/get', views_file.category_get, name='category_get'),
    path('categories/delete/<int:id>', views_file.category_delete, name='category_delete'),
    path('category/edit/<int:id>', views_file.category_edit, name='category_edit_api'),
    path('category/delete/<int:id>', views_file.category_delete, name='category_delete_api'),

    path('average/monthly', views_file.monthly_average, name='monthly_average'),
]
