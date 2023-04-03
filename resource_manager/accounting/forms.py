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
    cheque_receipt = forms.ModelChoiceField(queryset=OperationsChequeReceipt.objects.all(), required=False)
    
    class Meta:
        model = OperationsBudget
        fields = ['account', 'cheque_receipt', 'votehead', 'amount', 'date_budgeted']


    def save(self, *args, **kwargs):
        is_new = self.instance.pk is None  # Check if this is a newly created budget

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
        if kwargs.get('commit', True):
            budget.save()

        if is_new:
            # Create a new VoteHeadReceipt instance corresponding to the newly created budget
            votehead_receipt = VoteHeadReceipt(
                votehead=budget.votehead,
                amount=budget.amount,
                date_received=budget.date_budgeted
            )
            votehead_receipt.save()

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


#Payment Voucher
class PaymentVoucherForm(forms.ModelForm):
    class Meta:
        model = PaymentVoucher
        fields = ['date', 'payee_name', 'description', 'amount', 'payment_type', 'votehead', 'approved_by', 'voucher_number', 'cheque_number']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def save(self, *args, **kwargs):
        instance = super(PaymentVoucherForm, self).save(commit=False)

        # Set a default value for votehead
        votehead = instance.votehead

        if instance.payment_type == 'cash':
            instance.cheque_number = None
            # Deduct cash amount from OperationsCashAccount
            bank_account = votehead.account
            cash_account = OperationsCashAccount.objects.first()
            if bank_account.account_number == cash_account.account_number:
                cash_account.cash_balance -= instance.amount
                cash_account.total_balance = cash_account.cash_balance
                cash_account.save()
        else:
            # Check if a Cheque object with the same cheque_number exists
            cheque_exists = Cheque.objects.filter(cheque_number=instance.cheque_number).exists()

            if not cheque_exists:
                # Deduct cheque amount from OperationsBankAccount
                bank_account = votehead.account
                cheque_account = OperationsBankAccount.objects.first()
                if bank_account.account_number == cheque_account.account_number:
                    cheque_account.bank_balance -= instance.amount
                    cheque_account.total_balance = cheque_account.bank_balance
                    cheque_account.save()
                    instance.cheque_number = instance.cheque_number
                    
                    # Add the amount to the votehead
                    votehead.amount_spent += instance.amount
                    votehead.balance = votehead.amount_budgeted - votehead.amount_spent
                    votehead.save()
            else:
                instance.cheque_number = instance.cheque_number

        instance.save(*args, **kwargs)
        return instance
    

#cheque creation form
class ChequeForm(forms.ModelForm):
    class Meta:
        model = Cheque
        fields = ['payee_name', 'cheque_number', 'amount', 'date_issued', 'votehead', 'remarks']

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Set a default value for votehead
        votehead = instance.votehead

        # Check if a PaymentVoucher or PettyCash object with the same cheque_number exists
        payment_voucher_exists = PaymentVoucher.objects.filter(cheque_number=instance.cheque_number).exists()
        pettycash_exists = PettyCash.objects.filter(cheque_number=instance.cheque_number).exists()

        if not payment_voucher_exists and not pettycash_exists:
            # Deduct amount from the OperationsBankAccount
            bank_account = OperationsBankAccount.objects.first()
            bank_account.bank_balance -= instance.amount
            bank_account.total_balance = bank_account.bank_balance
            bank_account.save()

            # Add the amount to the votehead
            votehead.amount_spent += instance.amount
            votehead.balance = votehead.amount_budgeted - votehead.amount_spent
            votehead.save()

        if commit:
            instance.save()
        return instance
