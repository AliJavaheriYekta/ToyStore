from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


# Create your views here.
@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if username is not None and password is not None:
        user = User.objects.create_user(username, password=password)
        token = Token.objects.create(user=user)
        return Response({'token': token.key})
    else:
        return Response({'error': 'Username and password are required'})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect based on user role or request parameter
            if request.GET.get('next'):
                return redirect(request.GET['next'])
            elif user.is_staff:
                return redirect('/admin/')
            else:
                return redirect('/blog/')
        else:
            # Handle login failure
            pass
    return render(request, 'login.html')