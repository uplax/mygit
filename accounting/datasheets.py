# -*-coding: utf-8-*-
from __future__ import unicode_literals
import os, xlrd, xlwt
from models import Transaction, WorkGroup, Report
from django.db.models import Q

import StringIO
from django.core.files import File




def report_book(user,name,bills,start_date,stop_date):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    PATH = BASE_DIR +'/uploads/'+str(user)
    if not os.path.exists(PATH):
        os.makedirs(PATH)
    wb = xlwt.Workbook(encoding="UTF-8")
    for rt in bills:
        for bills in WorkGroup.objects.filter(pk=rt):
            ws = wb.add_sheet(str(bills.bill.bill_id), cell_overwrite_ok=True)
            style_head = "font: bold 1; align: horizontal center"
            style_data = "align: horizontal center;"
            head = xlwt.easyxf(style_head)
            cols = xlwt.easyxf(style_data)
            pattern = xlwt.Pattern()
            pattern.pattern = xlwt.Pattern.SOLID_PATTERN
            pattern.pattern_fore_colour = xlwt.Style.colour_map['light_green']
            border = xlwt.Borders()
            border.bottom = xlwt.Borders.MEDIUM
            border.top = xlwt.Borders.MEDIUM
            border.right = xlwt.Borders.MEDIUM
            border.left = xlwt.Borders.MEDIUM
            head.borders = border
            cols.borders = border
            cols.pattern = pattern
            ws.col(0).width = 3000
            ws.col(1).width = 2500
            ws.col(2).width = 2500
            ws.col(3).width = 2000
            ws.col(4).width = 5000
            ws.col(5).width = 5000
            ws.write(0, 0, 'Дата', style=head)
            ws.write(0, 1, 'Дебет', style=head)
            ws.write(0, 2, 'Кредит', style=head)
            ws.write(0, 3, 'Счет', style=head)
            ws.write(0, 4, 'Контрагент', style=head)
            ws.write(0, 5, 'Примечание', style=head)
            n=1
            for transaction in Transaction.objects.filter(Q(debit=bills) | Q(credit=bills)).filter(date__range=(start_date,stop_date)):
                ws.write(n, 0, str(transaction.date), style=cols)
                if str(transaction.debit.pk) == str(rt):
                    ws.write(n, 1, transaction.summ, style=cols)
                    ws.write(n, 2, '',style=cols)
                    ws.write(n, 3, str(transaction.credit.bill.bill_id), style=cols)
                elif str(transaction.credit.pk) == str(rt):
                    ws.write(n, 1, '',style=cols)
                    ws.write(n, 2, transaction.summ, style=cols)
                    ws.write(n, 3, str(transaction.debit.bill.bill_id), style=cols)
                ws.write(n, 4, str(transaction.contractor), style=cols)
                ws.write(n, 5, unicode(transaction.info),style=cols)
                n=n+1
    f = StringIO.StringIO()
    wb.save(f)
    r = Report(start_date=start_date,stop_date=stop_date,name=name,user=user)
    r.report.save(str(user)+'/'+name+'.xls',File(f))
    f.close()







