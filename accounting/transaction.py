# -*-coding: utf-8-*-
from __future__ import unicode_literals
from forms import *
from django.utils import timezone
from django.shortcuts import render
from django.http.response import HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/')
def transactions(request):
    trans = Transaction.objects.all()
    form = TransactionForm(request.user)
    if request.method == "POST":
        form = TransactionForm(user=request.user, data=request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.date = timezone.now()
            transaction.save()
            return HttpResponseRedirect(request.path)
    return render(
            request,
            'bookkeeper/transaction/transactions.html',
            {'form': form, 'trans': trans}
        )


@login_required(login_url='/login/')
def transaction_editor(request, pk):
    form = TransactionForm(
        request.user,
        request.POST or None,
        instance=pk and Transaction.objects.get(pk=pk)
    )
    if request.method == 'POST' and form.is_valid():
        form.save()
        next_page = request.GET.get('next', '/')
        return HttpResponseRedirect(next_page)
    return render(
        request,
        'bookkeeper/transaction/transaction_editor.html',
        {'form': form}
    )


@login_required(login_url='/login/')
def delete_transaction(request, pk):
    try:
        transaction = Transaction.objects.get(pk=pk)
        if transaction:
            if transaction.user == request.user:
                transaction.delete()
                return HttpResponseRedirect('/transactions/')
            else:
                return HttpResponseNotFound('<h1>Ошибка 404. Упс! Что-то пошло не так!</h4>')
    except:
        return HttpResponseNotFound('<h1>Ошибка 404. Упс! Что-то пошло не так!</h4>')
