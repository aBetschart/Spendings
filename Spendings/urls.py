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

from SpendingsApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    
    path('spending/submit/api', views.spending_submit_api, name='spending_submit_api'),
    path('spending/get/', views.spending_get, name='spending_get'),
    path('spending/get/recent', views.spending_get_recent_api, name='spending_get_recent'),
    path('spending/delete/api/<int:id>', views.spending_delete_api, name='spending_delete_api'),
    path('spending/edit/<int:id>', views.spending_edit, name='spending_edit'),
    path('spending/edit/api/<int:id>', views.spending_edit_api, name='spending_edit_api'),

    path('categories', views.categories, name='categories'),
    path('categories/edit/<int:id>', views.category_edit, name='category_edit'),
    path('categories/delete/<int:id>', views.category_delete, name='category_delete'),

    path('category/post', views.category_post, name='category_post'),
    path('category/get', views.category_get, name='category_get'),
    path('category/edit/api/<int:id>', views.category_edit_api, name='category_edit_api'),
    path('category/delete/api/<int:id>', views.category_delete_api, name='category_delete_api'),
    
    path('month', views.monthly_overview, name='monthly_overview'),
    path('year', views.yearly_overview, name='yearly_overview'),
]
