

from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import logout
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView

from SpendingsApp.views.auth_views import AuthenticatedView, AuthenticatedTemplateView


PASSWORD_MIN_LENGTH = 8


class RegisterView(TemplateView):
    template_name = 'register.html'

class AccountSettingsView(AuthenticatedTemplateView):
    template_name = 'settings.html'

class LogoutApi(AuthenticatedView):
    def post(self, request: HttpRequest) -> HttpResponse:
        try:
            logout(request)
        except Exception as e:
            return HttpResponseBadRequest(f"Error during logout: {str(e)}")
        return redirect('login')
    


class ChangePasswordApi(AuthenticatedView):

    NEW_PASSWORD_FIELD = 'NewPassword'
    OLD_PASSWORD_FIELD = 'OldPassword'
    def post(self, request: HttpRequest) -> HttpResponse:
        old_password = request.POST.get(self.OLD_PASSWORD_FIELD)
        if old_password is None:
            return HttpResponseBadRequest(f"Missing required field: '{self.OLD_PASSWORD_FIELD}'.")

        new_password = request.POST.get(self.NEW_PASSWORD_FIELD)
        if new_password is None:
            return HttpResponseBadRequest(f"Missing required field: '{self.NEW_PASSWORD_FIELD}'.")
        
        if not self._is_password_correct(request.user, old_password):
            return HttpResponseBadRequest("Old password is incorrect.")
        
        if not len(new_password) >= PASSWORD_MIN_LENGTH:
            return HttpResponseBadRequest(f"New password must be at least {PASSWORD_MIN_LENGTH} characters long.")

        try:
            user = request.user
            user.set_password(new_password)
            user.save()
        except Exception as e:
            return HttpResponseBadRequest(f"Error changing password: {str(e)}")
        
        return JsonResponse({'message': 'Password changed successfully.'}, status=200)
    
    def _is_password_correct(self, user: AbstractBaseUser, password: str) -> bool:
        return user.check_password(password)
    



class RegisterApi(View):
    USERNAME_FIELD = 'username'
    PASSWORD_FIELD = 'password'
    EMAIL_FIELD = 'email'

    def post(self, request: HttpRequest) -> HttpResponse:
        username = request.POST.get(self.USERNAME_FIELD)
        password = request.POST.get(self.PASSWORD_FIELD)
        email = request.POST.get(self.EMAIL_FIELD)
        if not username or not password or not email:
            return HttpResponseBadRequest("Username, password, and email are required.")

        username = username.strip()
        email = email.strip().lower()

        try:
            validate_password(password)
        except ValidationError as e:
            return HttpResponseBadRequest('; '.join(e.messages))
        
        if len(password) < PASSWORD_MIN_LENGTH:
            return HttpResponseBadRequest(f"Password must be at least {PASSWORD_MIN_LENGTH} characters long.")

        try:
            validate_email(email)
        except ValidationError:
            return HttpResponseBadRequest('Invalid email address.')

        user_model = get_user_model()
        if user_model.objects.filter(username=username).exists():
            return HttpResponseBadRequest("Username is already taken.")
        
        if user_model.objects.filter(email=email).exists():
            return HttpResponseBadRequest("Email is already registered.")
        
        try:
            user_model.objects.create_user(username=username, password=password, email=email)
        except Exception as e:
            return HttpResponseBadRequest(f"Error creating user: {str(e)}")
        
        return JsonResponse({'message': 'Registration successful.'}, status=201)
    
