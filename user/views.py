from django.contrib.auth.views import LogoutView, LoginView


class LoginViewCustom(LoginView):
	template_name = 'user/login.html'


class LogoutViewCustom(LogoutView):
	template_name = 'user/logout.html'
