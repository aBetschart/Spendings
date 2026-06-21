
from datetime import datetime

from SpendingsApp.forms import MonthlyOverviewForm, SpendingFilterForm, SpendingForm, MONTH_CHOICES, YearlyOverviewForm
from SpendingsApp.views.auth_views import AuthenticatedTemplateView

class HomeView(AuthenticatedTemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["spendingForm"] = SpendingForm(user=user)
        return context
    

class FilterView(AuthenticatedTemplateView):
    template_name = 'filter.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["spendingFilterForm"] = SpendingFilterForm()
        return context
    

class MonthView(AuthenticatedTemplateView):
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
    

class YearView(AuthenticatedTemplateView):
    template_name = 'year.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["year_form"] = self._setup_year_form()
        return context
    
    def _setup_year_form(self) -> YearlyOverviewForm:
        now = datetime.now()
        initial = { 'year': now.year }
        return YearlyOverviewForm(initial=initial)