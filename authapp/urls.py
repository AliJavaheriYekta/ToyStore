from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from authapp.views import register

urlpatterns = [
    path('register/', register),
    path('login/', obtain_auth_token),
]