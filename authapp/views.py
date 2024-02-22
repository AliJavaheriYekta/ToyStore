from django.contrib.auth.models import User
from django.shortcuts import render
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
