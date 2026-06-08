from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views import View


class AuthenticatedTemplateView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = 'next'


class AuthenticatedView(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'next'
