from django import forms
from .models import OperationsTransaction

class OperationsTransactionForm(forms.ModelForm):
    class Meta:
        model = OperationsTransaction
        fields = ['account', 'transaction_number', 'transaction_type', 'amount', 'payment_type']
