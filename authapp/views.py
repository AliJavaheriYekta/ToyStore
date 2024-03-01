from logging import getLogger

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from ToyStore.local_settings import ADMIN_PATH

from authapp.serializers import UserSerializer
from django.contrib.messages import info, error


# Create your views here.
@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if username is not None and password is not None:
        user = User.objects.create_user(username, password=password)
        if user:
            return Response({'success': 'User registered!'})
        # token = Token.objects.create(user=user)
        # return Response({'token': token.key})
        else:
            return Response({'error': 'User with this credential does not exist!'})
    else:
        return Response({'error': 'Username and password are required'})


def login_view(request):
    print("hey")
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                Token.objects.get(user=user)
            except:
                Token.objects.create(user=user)
            # Redirect based on user role or request parameter
            if request.GET.get('next'):
                return redirect(request.GET['next'])
            elif user.is_staff:
                return redirect(f'/{ADMIN_PATH}/')
            else:
                return redirect('/blog/')
        else:
            # Handle login failure
            pass
    return render(request, 'login.html')


def logout_view(request):
    """Logs out the current user and redirects to the home page."""
    if request.method == 'POST':
        logout(request)
        return redirect('/')
    else:
        logout(request)
        return redirect('/accounts/login')
        # return render(request, 'login.html', {'message': 'Please use POST request to logout.'})


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Registration successful!'}, status=201)
        else:
            return Response(serializer.errors, status=400)


logger = getLogger(__name__)


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # User registration logic
        if password != password2:
            error(request, 'Passwords do not match')
            return render(request, 'register.html')

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            info(request, 'Registration successful!')
            logger.info(f'User {username} registered successfully.')
            # return redirect('/')
            return redirect('/accounts/login')
        except Exception as e:
            error(request, f'Registration failed: {e}')
            logger.error(f'Registration failed for {username}: {e}')
            return render(request, 'register.html')

    return render(request, 'register.html')
