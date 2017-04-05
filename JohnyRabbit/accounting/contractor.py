# -*-coding: utf-8-*-
from __future__ import unicode_literals
from models import Contractor
from forms import ContractorForm
from django.shortcuts import render
from django.http.response import HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/')
def contractor_list(request):
    if request.method == 'POST':
        form = ContractorForm(data=request.POST)
        if form.is_valid():
            contractor = form.save(commit=False)
            contractor.user = request.user
            contractor.save()
            return HttpResponseRedirect(request.path)
    else:
        form = ContractorForm
    return render(request, 'bookkeeper/contractor/contractor_list.html', {'form': form})


@login_required(login_url='/login/')
def contractor_more(request, pk):
    contractor = Contractor.objects.filter(user=request.user).get(pk=pk)
    return render(request, 'bookkeeper/contractor/contractor_more.html', {'contractor': contractor})


@login_required(login_url='/login/')
def delete_contractor(request, pk):
    try:
        contractor = Contractor.objects.get(pk=pk)
        if contractor.user == request.user:
            contractor.delete()
            return HttpResponseRedirect('/contractor/')
        else:
            return HttpResponseNotFound('<h1>Ошибка 404. Упс! Что-то пошло не так!</h4>')
    except:
        return HttpResponseNotFound('<h1>Ошибка 404. Упс! Что-то пошло не так!</h4>')
