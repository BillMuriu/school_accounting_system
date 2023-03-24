from django import forms
from .models import *

class OperationsReceiptForm(forms.ModelForm):
    class Meta:
        model = OperationsReceipt
        fields = ['account', 'amount', 'receipt_type', 'date_received']
