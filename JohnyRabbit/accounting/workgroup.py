# -*-coding: utf-8-*-
from __future__ import unicode_literals
from forms import *
from django.shortcuts import render
from django.http.response import HttpResponseRedirect, HttpResponseNotFound
from django.db.models import Sum
from models import *
from django.contrib.auth.decorators import login_required
from decimal import *


@login_required(login_url='/login/')
def workgroup_list(request):
    objects = WorkGroup.objects.filter(user=request.user)
    work = []
    for item in objects:
        work.append(
            item.bill.bill_id
        )
    if request.method == 'POST':
        form = WorkGroupForm(workgroup=work, data=request.POST)
        if form.is_valid():
            workgroup = form.save(commit=False)
            workgroup.user = request.user
            workgroup.save()
            return HttpResponseRedirect(request.path)
    else:
        form = WorkGroupForm(workgroup=work)
    return render(
        request,
        'bookkeeper/workgroup/workgroup.html',
        {'form': form}
    )


@login_required(login_url='/login/')
def bill_more(request, pk):
    bill = Bill.objects.get(bill_id=pk)
    bill = WorkGroup.objects.get(bill=bill, user=request.user)
    debit_t = Transaction.objects.filter(user=request.user,debit=bill).aggregate(Sum('summ'))
    credit_t = Transaction.objects.filter(user=request.user,credit=bill).aggregate(Sum('summ'))
    try:
        if bill.bill.bill_type == 'Активный':
            if debit_t['summ__sum'] is None:
                saldo = Decimal(0)-credit_t['summ__sum']
            elif credit_t['summ__sum'] is None:
                saldo = debit_t['summ__sum'] - Decimal(0)
            else:
                saldo = debit_t['summ__sum'] - credit_t['summ__sum']
        elif bill.bill.bill_type == 'Пассивный':
            if debit_t['summ__sum'] is None:
                saldo = credit_t['summ__sum']-Decimal(0)
            elif credit_t['summ__sum'] is None:
                saldo = Decimal(0)-debit_t['summ__sum']
            else:
                saldo = credit_t['summ__sum'] - debit_t['summ__sum']
        else:
            if debit_t['summ__sum'] is None:
                saldo = Decimal(0) - credit_t['summ__sum']
            elif credit_t['summ__sum'] is None:
                saldo = debit_t['summ__sum'] - Decimal(0)
            else:
                saldo = debit_t['summ__sum'] - credit_t['summ__sum']
    except Exception:
        saldo = 0
    return render(
        request,
        'bookkeeper/workgroup/bill_more.html',
        {'bill': bill, 'saldo': saldo, 'sal': debit_t}
    )


@login_required(login_url='/login/')
def delete_bill(request, pk):
    try:
        bill = Bill.objects.get(bill_id=pk)
        workgroup = WorkGroup.objects.get(user=request.user,bill=bill)
        if workgroup.user == request.user:
            workgroup.delete()
            return HttpResponseRedirect('/workgroup/')
    except:
        return HttpResponseNotFound('ss')