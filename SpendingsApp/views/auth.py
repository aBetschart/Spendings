

from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth import logout
from django.shortcuts import redirect

from SpendingsApp.views.auth_views import AuthenticatedView, AuthenticatedTemplateView

class AccountSettingsView(AuthenticatedTemplateView):
    template_name = 'settings.html'

class LogoutApi(AuthenticatedView):
    def post(self, request: HttpRequest) -> HttpResponse:
        try:
            logout(request)
        except Exception as e:
            return HttpResponseBadRequest(f"Error during logout: {str(e)}")
        return redirect('login')
    

NEW_PASSWORD_FIELD = 'NewPassword'
OLD_PASSWORD_FIELD = 'OldPassword'

PASSWORD_MIN_LENGTH = 8

class ChangePasswordApi(AuthenticatedView):
    def post(self, request: HttpRequest) -> HttpResponse:
        old_password = request.POST.get(OLD_PASSWORD_FIELD)
        if old_password is None:
            return HttpResponseBadRequest(f"Missing required field: '{OLD_PASSWORD_FIELD}'.")

        new_password = request.POST.get(NEW_PASSWORD_FIELD)
        if new_password is None:
            return HttpResponseBadRequest(f"Missing required field: '{NEW_PASSWORD_FIELD}'.")
        
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
    

