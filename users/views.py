from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView


class LoginViewCustom(LoginView):
    template_name = 'users/login.html'

class LogoutViewCustom(LoginRequiredMixin, LogoutView):
    template_name = 'users/logout.html'