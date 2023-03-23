from django import forms
from .models import *

class OperationsTransactionForm(forms.ModelForm):
    class Meta:
        model = OperationsTransaction
        fields = ['account', 'votehead', 'amount', 'payment_type']

class OperationsReceiptForm(forms.ModelForm):
    class Meta:
        model = OperationsReceipt
        fields = ['account', 'amount', 'receipt_type', 'date_received']
