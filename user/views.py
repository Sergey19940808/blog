from django.contrib.auth.views import LogoutView, LoginView

class LoginViewCustom(LoginView):
    template_name = 'users/login.html'

class LogoutViewCustom(LogoutView):
    template_name = 'users/logout.html'