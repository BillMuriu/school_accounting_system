from django import forms
from .models import *

class ChequeReceiptForm(forms.ModelForm):
    class Meta:
        model = OperationsChequeReceipt
        fields = ['account', 'received_from', 'amount', 'date_received']
        widgets = {
            'account': forms.Select(attrs={'class': 'form-control'}),
            'received_from': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'date_received': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }

    def save(self, commit=True):
        instance = super(ChequeReceiptForm, self).save(commit=False)
        account = instance.account
        amount = instance.amount

        account.bank_balance += amount
        account.total_balance = account.bank_balance

        if commit:
            instance.save()
            account.save()

        return instance



class OperationsBudgetForm(forms.ModelForm):
    class Meta:
        model = OperationsBudget
        fields = ['account', 'votehead', 'amount', 'date_budgeted']