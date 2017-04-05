from __future__ import unicode_literals
from models import *
from django.http.response import HttpResponseRedirect
from forms import *
from django.shortcuts import render


def workgroup(request):
    if WorkGroup.objects.filter(user=request.user).exists():
        return HttpResponseRedirect('/')
    else:
        form = FirstWorkgroup()
        if request.method == 'POST':
            bills = request.POST['bills']
            for bill in bills:
                print bill
                b = Bill.objects.get(pk=bill)
                workgroup = WorkGroup(user=request.user,
                                      bill=b)
                workgroup.save()
            return HttpResponseRedirect('/')
    return render(request,'bookkeeper/routers/workgroup.html', {'form': form})
