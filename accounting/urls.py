# -*-coding: utf-8-*-
from __future__ import unicode_literals
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
import index, ajaxdata, contractor, report, transaction, workgroup, user,routers


urlpatterns = [
    # index pages
    url(r'^$',
        index.index,
        name='index'),
    url(r'^index/$',
        index.index,
        name='index'),
    # transactions
    url(r'^transactions/$',
        transaction.transactions,
        name='main'),
    # transactions ajax data
    url(r'^ajaxdata/transactions$',
        login_required(ajaxdata.TransactionJson.as_view()),
        name='trans_data'),
    # contractors ajax data
    url(r'^ajaxdata/contractors$',
        login_required(ajaxdata.ContractorData.as_view()),
        name='contr_data'),
    # workgroup ajax data
    url(r'^ajaxdata/workgroup$',
        login_required(ajaxdata.WorkGroupData.as_view()),
        name='workgroup_data'),
    # contractors
    url(r'^ajaxdata/transactionsc/(?P<pk>[0-9]+)/$',
        login_required(ajaxdata.TransactionJsonContractor.as_view()),
        name='transc_data'),
    url(r'^ajaxdata/transactionsb/(?P<pk>[0-9]+)/$',
        login_required(ajaxdata.BillData.as_view()),
        name='transb_data'),
    url(r'^ajaxdata/reports$',
        login_required(ajaxdata.ReportData.as_view()),
        name='report_data'),
    url(r'^contractor/$',
        contractor.contractor_list,
        name='contractor_more'),
    # workgroup
    url(r'^workgroup/$',
        workgroup.workgroup_list,
        name='workgroup'),
    # look more
    url(r'^contractor/(?P<pk>[0-9]+)/$',
        contractor.contractor_more,
        name='contr_more'),
    url(r'^workgroup/bill/(?P<pk>[0-9]+)/$',
        workgroup.bill_more,
        name='bill'),
    # remove objects
    url(r'^removetransaction/(?P<pk>[0-9,a-z,а-я]+)/$',
        transaction.delete_transaction,
        name='delete_t'),
    url(r'^removecontractor/(?P<pk>[0-9]+)/$',
        contractor.delete_contractor,
        name='delete_c'),
    url(r'^removeworkgroup/(?P<pk>[0-9]+)/$',
        workgroup.delete_bill,
        name='delete_b'),
    url(r'^removereport/(?P<pk>[0-9]+)/$',
        report.report_remove,
        name='delete_r'),
    url(r'^edittrans/(?P<pk>[0-9]+)/$',
        transaction.transaction_editor,
        name='edit_s'),
    url(r'^reports/$',
        report.reports,
        name='reports'),
    url(r'^media/(?P<path>.*)$', report.report_download, name='download'),
    url(r'^register/$', user.register, name='register'),
    url(r'^login/$', user.login_view, name='login'),
    url(r'^logout/$', user.logout_view, name='logout'),
    url(r'^routers/$', routers.workgroup , name='routers')
]
