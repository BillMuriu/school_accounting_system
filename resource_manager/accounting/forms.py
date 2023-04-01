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