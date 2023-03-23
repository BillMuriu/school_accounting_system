from django import forms
from .models import *

class OperationsTransactionForm(forms.ModelForm):
    class Meta:
        model = OperationsTransaction
        fields = ['account', 'votehead', 'amount', 'payment_type']

class OperationsReceiptForm(forms.ModelForm):
    class Meta:
        model = OperationsReceipt
        fields = ['account_number', 'amount', 'receipt_type', 'date_received']

    def clean(self):
        cleaned_data = super().clean()
        receipt_type = cleaned_data.get("receipt_type")
        account_number = cleaned_data.get("account_number")
        if receipt_type == "cheque" and not account_number.startswith("B"):
            raise forms.ValidationError("Invalid account number for cheque receipt")
        return cleaned_data
