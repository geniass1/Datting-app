from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import NewUser
import jwt

from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import UserSerializer, ChangeSerializer


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # breakpoint()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main:main')
        else:
            messages.info(request, 'Password or username is incorrect')
    context = {}
    return render(request, 'user/login.html', context)


def logout_page(request):
    logout(request)
    return redirect('user:login')


@csrf_exempt
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Accaunt was created')
            return redirect('user:login')
    context = {'form': form}
    return render(request, 'user/register.html', context)


class Register(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class ChangeInfo(APIView):
    def post(self, request, *args, **kwargs):
        user = NewUser.objects.get(username=request.data['username'])
        serializer = ChangeSerializer(data=request.data, instance=user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class Login(APIView):
    def post(self, request):
        if NewUser.objects.get(username=request.data['username']).check_password(request.data['password']):
            key = "secret"
            encoded = jwt.encode({"username": request.data['username']}, key, algorithm="HS256")
            return Response(encoded)


def change_user_info(request):
    if request.method == 'POST':
        username = request.POST.get('old_username')
        password = request.POST.get('old_password')
        new_username = request.POST.get('new_username')
        new_password = request.POST.get('new_password')
        user = NewUser.objects.get(username=username)
        if user.check_password(password):
            user.username = new_username
            user.set_password(new_password)
            user.save()
            return redirect('user:login')
        else:
            messages.info(request, 'password is incorrect')
    return render(request, 'user/change_user_info.html')