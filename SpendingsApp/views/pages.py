
from django.views.generic import TemplateView

from SpendingsApp.forms import SpendingFilterForm, SpendingForm

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["spendingForm"] = SpendingForm()
        return context
    

class FilterView(TemplateView):
    template_name = 'filter.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["spendingFilterForm"] = SpendingFilterForm()
        return context
    