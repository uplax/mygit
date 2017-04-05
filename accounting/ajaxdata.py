from __future__ import unicode_literals
from django_datatables_view.base_datatable_view import BaseDatatableView
from models import *
from django.db.models import Q


class TransactionJson(BaseDatatableView):
    model = Transaction
    columns = ['pk', 'date', 'debit', 'credit',
               'summ', 'contractor', 'info']
    order_columns = ['date', 'debit', 'credit',
                     'summ', 'contractor', 'info']
    max_display_length = 500

    def get_initial_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                "pk": item.pk,
                "contr_id": item.contractor.id,
                "date": item.date.strftime('%d-%m-%Y'),
                "debit": str(item.debit)[:2],
                "credit": str(item.credit)[:2],
                "summ": str(item.summ),
                "contractor":
                    {"name": str(item.contractor),
                     "id": item.contractor.pk},
                "info": item.info
            })
        return json_data


class ContractorData(BaseDatatableView):
    model = Contractor
    columns = ['organization', 'name', 'inn', 'pk']
    order_columns = ['organization', 'name', 'inn']
    max_display_length = 200

    def get_initial_queryset(self):
        return Contractor.objects.filter(user=self.request.user)

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                "organization": item.organization,
                "name": item.name,
                "inn": item.inn,
                "pk": item.pk
            })
        return json_data


class WorkGroupData(BaseDatatableView):
    model = WorkGroup
    columns = ['bill', 'bill', 'bill', 'bill']
    order_columns = ['bill', 'bill', 'bill']

    def get_initial_queryset(self):
        return WorkGroup.objects.filter(user=self.request.user)

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                "bill_id": item.bill.bill_id,
                "bill_info": item.bill.bill_name,
                "bill_type": item.bill.bill_type,
                'id': item.bill.id
            })
        return json_data


class TransactionJsonContractor(BaseDatatableView):
    model = Transaction
    columns = ['pk', 'date', 'debit', 'credit',
               'summ', 'contractor', 'info']
    order_columns = ['date', 'debit', 'credit',
                     'summ', 'contractor', 'info']
    max_display_length = 500

    def get_initial_queryset(self, **kwargs):
        contractor = Contractor.objects.get(pk=self.kwargs['pk'])
        transactions = Transaction.objects.filter(contractor=contractor)
        return transactions

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                "pk": item.pk,
                "contr_id": item.contractor.id,
                "date": item.date.strftime('%d-%m-%Y'),
                "debit": str(item.debit)[:2],
                "credit": str(item.credit)[:2],
                "summ": str(item.summ),
                "contractor":
                    {"name": str(item.contractor),
                     "id": item.contractor.inn},
                "info": item.info
            })
        return json_data


class BillData(BaseDatatableView):
    model = Transaction
    columns = [
        'date',
        'debit',
        'credit',
        'summ',
        'contractor',
        'info',
        'pk'
    ]
    order_columns = ['date', 'debit', 'credit',
                     'summ', 'contractor', 'info']

    def get_initial_queryset(self):
        bill = Bill.objects.get(bill_id=self.kwargs['pk'])
        workgroup = WorkGroup.objects.get(bill=bill, user=self.request.user)
        transaction = Transaction.objects.filter(user=self.request.user).filter(
            Q(debit=workgroup) | Q(credit=workgroup))
        return transaction

    def prepare_results(self, qs):
        bill = self.kwargs['pk']
        json_data = []
        for item in qs:
            json_data.append({
                'pk': item.pk,
                'date': item.date.strftime('%d-%m-%Y'),
                'bill': str(item.debit)[:2] if str(bill) in str(item.credit) else str(item.credit)[:2],
                'debit': item.summ if str(bill) in str(item.debit) else '',
                'credit': item.summ if str(bill) in str(item.credit) else '',
                'contractor': {"name": str(item.contractor),
                               "id": item.contractor.pk},
                'info': item.info
            })
        return json_data


class ReportData(BaseDatatableView):
    model = Report
    columns = [
        'date_report',
        'name',
        'start_date',
        'stop_date',
        'report'
    ]
    order_columns = [
        'date_report',
        'name',
        'start_date',
        'stop_date',
        'report'
    ]

    def get_initial_queryset(self):
        report = Report.objects.filter(user=self.request.user)
        return report

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'date_report': item.date_report,
                'name': item.name,
                'start_date': item.start_date,
                'stop_date': item.stop_date,
                'report': str(item.filename),
                'url': {
                    'url': item.report.url,
                    'pk': item.pk
                }
            })
        return json_data
