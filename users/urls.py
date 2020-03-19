from django.urls import path

from users.views import LogoutViewCustom, LoginViewCustom

urlpatterns = [
    path('login/', LoginViewCustom.as_view(), name='login'),
    path('logout/', LogoutViewCustom.as_view(), name='logout'),
]