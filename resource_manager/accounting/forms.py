from django import forms
from .models import OperationsTransaction

class OperationsTransactionForm(forms.ModelForm):
    class Meta:
        model = OperationsTransaction
        fields = ['account', 'votehead', 'amount', 'payment_type']

