
from datetime import datetime

from django.views.generic import TemplateView

from SpendingsApp.forms import MonthlyOverviewForm, SpendingFilterForm, SpendingForm, MONTH_CHOICES, YearlyOverviewForm

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
    

class MonthView(TemplateView):
    template_name = 'month.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["monthForm"] = self._setup_month_form(datetime.now())
        return context
    
    def _setup_month_form(self, month_of_year: datetime) -> MonthlyOverviewForm:
        monthIndex = month_of_year.month - 1
        initial = {
            'month': MONTH_CHOICES[monthIndex][0],
            'year': month_of_year.year
        }
        return MonthlyOverviewForm(initial=initial)
    

class YearView(TemplateView):
    template_name = 'year.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["year_form"] = self._setup_year_form()
        return context
    
    def _setup_year_form(self) -> YearlyOverviewForm:
        now = datetime.now()
        initial = { 'year': now.year }
        return YearlyOverviewForm(initial=initial)