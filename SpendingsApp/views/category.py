
from http import HTTPStatus
from unicodedata import category

from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.generic import TemplateView, View
from django.shortcuts import render
from django.forms.models import model_to_dict

from SpendingsApp.forms import CategoryForm
from SpendingsApp.models import Category

from .util import get_category_from_id, is_category_name_used, is_category_used

# ------------------------------
# ---------- Views 
# ------------------------------


class CategoryOverview(TemplateView):
    template_name = 'categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categoryForm"] = CategoryForm()
        context["categories"] = Category.objects.order_by('name')        
        return context
    
class CategoryEditView(View):
    template_name = 'category.html'

    def get(self, request: HttpRequest, id: int) -> HttpResponse:
        try:
            category = get_category_from_id(id)
        except ValueError as error:
            return HttpResponseBadRequest(str(error))
        
        category_form = CategoryForm(instance=category)
        context = {"categoryForm": category_form}
        return render(request, self.template_name, context)
                      
# ------------------------------
# ---------- API
# ------------------------------

class CategoryEditApi(View):
    def post(self, request: HttpRequest, id: int) -> HttpResponse:
        try:
            category = get_category_from_id(id)
        except ValueError as error:
            return HttpResponseBadRequest(str(error))
        
        category_form = CategoryForm(request.POST, instance=category)
        if not category_form.is_valid():
            return HttpResponseBadRequest(f"Invalid form data: {category_form.errors}")
        
        name = category_form.cleaned_data['name']
        if is_category_name_used(name):
            return HttpResponseBadRequest(f"Another category already has the name '{name}'.")

        category_form.save()

        category_dict = model_to_dict(category)
        message = f"Category with id {id} edited successfully."
        response_data = {"message": message, "category": category_dict}
        return JsonResponse(response_data, status=HTTPStatus.OK)


class CategoryDeleteApi(View):
    def post(self, request: HttpRequest, id: int) -> HttpResponse:
        try:
            category = get_category_from_id(id)
        except ValueError as error:
            return HttpResponseBadRequest(str(error))
        
        if is_category_used(category):
            message = f"Category with id {id} is currently in use and cannot be deleted."
            return HttpResponseBadRequest(message)

        category.delete()

        message = f"Category with id {id} deleted successfully."
        response_data = {"message": message}
        return JsonResponse(response_data, status=HTTPStatus.OK)
    
class CategoryGetApi(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        categories = Category.objects.order_by('name')
        category_list = [model_to_dict(category) for category in categories]
        response_data = {"categories": category_list}
        return JsonResponse(response_data, safe=False, status=HTTPStatus.OK)


class CategoryPostApi(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        category_form = CategoryForm(request.POST)
        if not category_form.is_valid():
            return HttpResponseBadRequest(f"Invalid form data: {category_form.errors}")
        
        name = category_form.cleaned_data['name']
        if is_category_name_used(name):
            return HttpResponseBadRequest(f"Category with name '{name}' already exists.")

        new_cateogry = category_form.save()

        category_dict = model_to_dict(new_cateogry)
        message = "Category created successfully"
        response_data = {"message": message, "category": category_dict}
        return JsonResponse(response_data, status=HTTPStatus.OK)