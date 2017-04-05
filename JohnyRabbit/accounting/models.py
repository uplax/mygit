# -*-coding: utf-8-*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
import os
from django.conf import settings

class Bill(models.Model):
    TYPE = (
        ('Активный',          'active'),
        ('Пассивный',         'passive'),
        ('Активно-Пассивный', 'active_passive')
    )
    bill_id = models.CharField(
        max_length=2,
        verbose_name='Номер счета'
    )
    bill_name = models.CharField(
        max_length=99,
        verbose_name='Наименование счета',
        null=True,
        blank=True
    )
    bill_type = models.CharField(
        max_length=30,
        choices=TYPE,
        verbose_name='Тип счета',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Счет'
        verbose_name_plural = 'Счета'

    def __unicode__(self):
        return '%s - %s' % (self.bill_id, self.bill_name)


class WorkGroup(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Книга'
    )
    bill = models.ForeignKey(
        Bill,
        verbose_name='Счет'
    )

    class Meta:
        verbose_name = 'Рабочая группа'
        verbose_name_plural = 'Рабочие группы'

    def __unicode__(self):
        return '%s'%self.bill.bill_id


class Contractor(models.Model):
    TYPE = (
        ('ИП', 'ИП'),
        ('ООО', 'ООО'),
        ('ОАО', 'ОАО')
    )
    organization = models.CharField(
        max_length=3,
        choices=TYPE,
        verbose_name='Организация'
    )
    name = models.CharField(
        max_length=30,
        verbose_name='Наименование'
    )
    inn = models.CharField(
        max_length=20,
        verbose_name='ИНН'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Контрагент'
        verbose_name_plural = 'Контрагенты'

    def __unicode__(self):
        return '%s %s %s'%(self.organization,self.name,self.inn)


class Transaction(models.Model):
    date = models.DateField(
        default= datetime.today(),
        verbose_name='Дата и время',
    )
    debit = models.ForeignKey(
        WorkGroup,
        related_name='debet',
        verbose_name='Дебет',
        on_delete=models.CASCADE,
        default=None
    )
    credit = models.ForeignKey(
        WorkGroup,
        related_name='credit',
        verbose_name='Кредит',
        on_delete=models.CASCADE,
        default=None
    )
    summ = models.DecimalField(
        decimal_places=2,
        max_digits=20,
        verbose_name='Сумма',
        default=None
    )
    contractor = models.ForeignKey(
        Contractor,
        verbose_name='Контрагент',
        on_delete=models.CASCADE,
        default=None
    )
    info = models.CharField(
        max_length=50,
        verbose_name='Информация',
        default=None
    )
    user = models.ForeignKey(
        User,
        default=None
    )

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'


class TransactionManager(models.Manager):
    def get_query_set(self):
        default_queryset = super(TransactionManager,self).get_query_set()
        return  default_queryset.filter(disabled=None).order_by('-date')

    def by_user(self, user):
        return super(TransactionManager, self).get_query_set().filter(user=user)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Report(models.Model):
    date_report = models.DateField(
        default= datetime.today(),
        verbose_name='Дата',
        null=True,
        blank=True
    )
    start_date = models.DateField(
        default=None,
        verbose_name='начало периода',
        null=True,
        blank=True
    )
    stop_date = models.DateField(
        default=None,
        verbose_name='Конец периода',
        null=True,
        blank=True
    )
    name = models.CharField(
        max_length=50,
        verbose_name='Наименование отчета',
        null=True,
        blank=True
    )
    bills = models.ManyToManyField(
        WorkGroup,
        verbose_name='Счета',
        related_name='bills',
        null=True,
        blank=True
    )
    report = models.FileField(
        verbose_name='Файл отчета',
        upload_to=BASE_DIR+'/uploads/',
        null=True,
        blank=True
    )
    user = models.ForeignKey(User)

    def filename(self):
        return os.path.basename(self.report.name)

    @property
    def relative_path(self):
        return os.path.realpath(self.path,settings.MEDIA_ROOT)




