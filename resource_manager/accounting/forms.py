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

    def save(self, commit=True):
        budget = super().save(commit=False)

        # Update account balance
        account = budget.account
        votehead_amount = budget.amount
        if account.total_balance < votehead_amount:
            raise ValueError(f"Insufficient funds in account {account.account_number}")
        if account.bank_balance < votehead_amount:
            raise ValueError(f"Insufficient bank funds in account {account.account_number}")
        account.bank_balance -= votehead_amount
        account.total_balance = account.bank_balance
        account.save()

        # Update votehead amount_budgeted
        votehead = budget.votehead
        votehead.amount_budgeted += votehead_amount
        votehead.save()

        # Save budget
        if commit:
            budget.save()

        return budget


#PettyCash form
class PettyCashForm(forms.ModelForm):
    class Meta:
        model = PettyCash
        fields = ['payee_name', 'cheque_number', 'amount', 'date_issued', 'operations_account']

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Check if a cheque with the same cheque_number already exists
        try:
            existing_cheque = Cheque.objects.get(cheque_number=instance.cheque_number)
            # If an existing cheque is found, do not deduct the amount from the bank account
        except Cheque.DoesNotExist:
            # If an existing cheque is not found, deduct the amount from the bank account
            # create a new OperationsCashReceipt
            operations_receipt = OperationsCashReceipt.objects.create(
                account=instance.operations_account,
                received_from=instance.payee_name,
                amount=instance.amount,
                date_received=instance.date_issued
            )

            # update the related OperationsCashAccount
            operations_account = instance.operations_account
            operations_account.total_balance = operations_account.cash_balance
            operations_account.save()

            # Deduct amount from the OperationsBankAccount
            bank_account = OperationsBankAccount.objects.first()
            bank_account.bank_balance -= instance.amount
            bank_account.total_balance = bank_account.bank_balance
            bank_account.save()

        if commit:
            instance.save()
        return instance


#PaymentVoucher Form
class PaymentVoucherForm(forms.ModelForm):
    class Meta:
        model = PaymentVoucher
        fields = ['date', 'payee_name', 'description', 'amount', 'payment_type', 'votehead', 'approved_by', 'voucher_number', 'cheque_number']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }