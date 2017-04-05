# -*-coding: utf-8-*-
from __future__ import unicode_literals
from forms import *
from django.shortcuts import render
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, logout, login
from models import *


def register(request):
    form = RegisterForm
    if request.method == 'POST':
        try:
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            user = User.objects.create_user(username, email, password)
            user.save()
            return HttpResponseRedirect('/index')
        except:
            return HttpResponse('<h1>Пользователь с таким именем уже существует<h1>')
    return render(request, 'bookkeeper/user/register.html', {'form': form})


def login_view(request):
    form = LoginForm
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/index')

    return render(request, 'bookkeeper/user/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')
