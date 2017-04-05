# -*-coding: utf-8-*-
from __future__ import unicode_literals
from forms import *
from django.shortcuts import render
from django.http.response import HttpResponseRedirect, HttpResponseNotFound, HttpResponse, Http404
from datasheets import report_book
import os
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/')
def reports(request):
    if request.method == 'POST':
        report_book(request.user,
                    request.POST['name'],
                    request.POST['bills'],
                    request.POST['start_date'],
                    request.POST['stop_date'])
        return HttpResponseRedirect(request.path)
    else:
        report = ReportForm(request.user)
    repos = Report.objects.filter(user=request.user)
    return render(
        request,
        'bookkeeper/report/reports.html',
        {'form': report, 'repos': repos})


@login_required(login_url='/login/')
def report_download(path):
    file_path = os.path.join('/media/', path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename='+os.path.basename(file_path)
            return response
    else:
        raise Http404


@login_required(login_url='/login/')
def report_remove(request, pk):
    report = Report.objects.get(pk=pk)
    if report.user == request.user:
        os.remove(report.report.name)
        report.delete()
        return HttpResponseRedirect('/reports/')
    else:
        return HttpResponseNotFound('<h1>Косяк с пользователем</h4>')
