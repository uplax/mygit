# -*-coding: utf-8-*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from models import *
from django.http.response import HttpResponseRedirect

@login_required(login_url='/login/')
def index(request):
    return render(request, 'bookkeeper/index.html')
