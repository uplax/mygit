from django.forms import ModelForm, Select
from django import forms
from models import *


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = (
            'debit',
            'credit',
            'summ',
            'contractor',
            'info',
        )

    def __init__(self ,user=None, *args,**kwargs ):
        # type: (self, user, data) -> form
        super(TransactionForm, self).__init__(*args,**kwargs)
        if user:
            self.fields['debit'].queryset = WorkGroup.objects.filter(user=user).order_by('bill')
            self.fields['debit'].widget.attrs['class'] = 'chosen'
            self.fields['credit'].queryset = WorkGroup.objects.filter(user=user).order_by('bill')
            self.fields['credit'].widget.attrs['class'] = 'chosen'
            self.fields['contractor'].queryset = Contractor.objects.filter(user=user)
            self.fields['contractor'].widget.attrs['class'] = 'chosen'
            self.fields['info'].widget.attrs['class'] = 'info'


class ContractorForm(ModelForm):
    class Meta:
        model = Contractor
        fields = (
            'organization',
            'name',
            'inn'
        )

    def __init__(self, *args, **kwargs):
        super(ContractorForm, self).__init__(*args,**kwargs)
        self.fields['organization'].widget.attrs['class'] = 'chosen'
        self.fields['name'].widget.attrs['class'] = 'info'
        self.fields['inn'].widget.attrs['class'] = 'info'


class WorkGroupForm(ModelForm):
    class Meta:
        model = WorkGroup
        fields = ('bill',)

    def __init__(self, workgroup=None, *args, **kwargs):
        super(WorkGroupForm, self).__init__(*args, **kwargs)
        self.fields['bill'].queryset = Bill.objects.exclude(bill_id__in=workgroup)
        self.fields['bill'].widget.attrs['class'] = 'chosen'


class ReportForm(forms.Form):
    name = forms.CharField(max_length=50)
    bills = forms.ModelMultipleChoiceField(queryset=WorkGroup.objects.all())
    start_date = forms.DateField()
    stop_date = forms.DateField()

    def __init__(self,user,*args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        self.fields['bills'].queryset = WorkGroup.objects.filter(user=user).order_by('bill')
        self.fields['bills'].widget.attrs['class'] = 'chosen'
        self.fields['start_date'].widget.attrs['class'] = 'date info'
        self.fields['name'].widget.attrs['class'] = 'info'
        self.fields['stop_date'].widget.attrs['class'] = 'date info'




class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)

    def __init__(self,*args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'info'
        self.fields['email'].widget.attrs['class'] = 'info'
        self.fields['password'].widget.attrs['class'] = 'info'

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)

    def __init__(self,*args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'info'
        self.fields['password'].widget.attrs['class'] = 'info'


class FirstWorkgroup(forms.Form):
    bills = forms.ModelMultipleChoiceField(queryset=Bill.objects.all())

    def __init__(self, *args, **kwargs):
        super(FirstWorkgroup, self).__init__(*args, **kwargs)
        self.fields['bills'].widget.attrs['class'] = 'chosen'
