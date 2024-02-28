from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from authapp.views import register, login_view, logout_view, register_view

app_name = 'auth'

urlpatterns = [
    path('register/', register),
    path('login/', obtain_auth_token),
    # path('logout/', obtain_auth_token),
    # path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/login/', login_view, name='login'),
    path('accounts/logout/', logout_view, name='logout'),
    path('accounts/register/', register_view, name='register'),
]