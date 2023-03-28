from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal



# Create your models here.

class OperationsCashAccount(models.Model):
    account_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=50)
    cash_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class OperationsBankAccount(models.Model):
    account_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=50)
    bank_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    month_end_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class OperationsCashReceipt(models.Model):
    account = models.ForeignKey(OperationsCashAccount, on_delete=models.CASCADE, default=None)
    received_from = models.CharField(max_length=100, default='')
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    date_received = models.DateField()

    def __str__(self):
        return f"Receipt {self.id} for {self.account.account_number} (Cash)"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        account = self.account
        amount = self.amount

        account.cash_balance += amount
        account.total_balance = account.cash_balance
        account.save()


class OperationsChequeReceipt(models.Model):
    account = models.ForeignKey(OperationsBankAccount, on_delete=models.CASCADE, default=None)
    received_from = models.CharField(max_length=100, default='')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_received = models.DateField()

    def __str__(self):
        return f"Receipt {self.id} for {self.account.account_number} (Cheque)"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        account = self.account
        amount = self.amount

        account.bank_balance += amount
        account.total_balance = account.bank_balance
        account.save()


class PettyCash(models.Model):
    payee_name = models.CharField(max_length=100, default='')
    cheque_number = models.CharField(max_length=20, unique=True, default='')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_issued = models.DateField()
    operations_account = models.ForeignKey(OperationsCashAccount, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"Petty Cash - {self.amount} ({self.date_issued}) - Payee: {self.payee_name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # create a new OperationsCashReceipt
        operations_receipt = OperationsCashReceipt.objects.create(
            account=self.operations_account,
            received_from=self.payee_name,
            amount=self.amount,
            date_received=self.date_issued
        )

        # update the related OperationsCashAccount
        operations_account = self.operations_account
        operations_account.cash_balance += self.amount
        operations_account.total_balance = operations_account.cash_balance
        operations_account.save()









class VoteHead(models.Model):
    ACCOUNT_TYPES = (
        ('operations', 'Operations Account'),
        ('other', 'Other Account'),
    )

    name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, default='other')
    account_number = models.CharField(max_length=20, unique=True, default='')
    account = models.ForeignKey(OperationsBankAccount, on_delete=models.CASCADE, default=None)
    amount_budgeted = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    def __str__(self):
        return self.name




class OperationsBudget(models.Model):
    account = models.ForeignKey(OperationsBankAccount, on_delete=models.CASCADE)
    votehead = models.ForeignKey(VoteHead, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_budgeted = models.DateField()

    def __str__(self):
        return f"{self.votehead} budgeted {self.amount} for {self.account.account_number}"

    def save(self, *args, **kwargs):
        # Update account balance
        account = self.account
        votehead = self.votehead
        votehead_amount = self.amount
        if account.total_balance < votehead_amount:
            raise ValueError(f"Insufficient funds in account {account.account_number}")
        if account.bank_balance < votehead_amount:
            raise ValueError(f"Insufficient bank funds in account {account.account_number}")
        account.bank_balance -= votehead_amount
        account.total_balance = account.bank_balance
        account.save()

        # Update votehead amount_budgeted
        votehead.amount_budgeted += votehead_amount
        votehead.save()

        # Save budget
        super().save(*args, **kwargs)

        # Send signal to update corresponding VoteHeadReceipt
        budget_updated.send(sender=self.__class__, budget=self)



class VoteHeadReceipt(models.Model):
    votehead = models.ForeignKey(VoteHead, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_received = models.DateField()

    def __str__(self):
        return f"Receipt for {self.votehead} ({self.amount})"


# Create signal for updating VoteHeadReceipt
budget_updated = Signal()

# Define receiver function for signal
@receiver(budget_updated, sender=OperationsBudget)
def update_votehead_receipt(sender, budget, **kwargs):
    # Find corresponding VoteHeadReceipt and update amount
    try:
        receipt = VoteHeadReceipt.objects.get(votehead=budget.votehead)
        receipt.amount += budget.amount
        receipt.save()
    except VoteHeadReceipt.DoesNotExist:
        # Create new VoteHeadReceipt if one does not exist
        receipt = VoteHeadReceipt.objects.create(votehead=budget.votehead, amount=budget.amount, date_received=budget.date_budgeted)


class PaymentVoucher(models.Model):
    PAYMENT_TYPES = (
        ('cash', 'Cash'),
        ('cheque', 'Cheque'),
    )

    date = models.DateField()
    payee_name = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES, default='cash')
    votehead = models.ForeignKey(VoteHead, on_delete=models.CASCADE)
    approved_by = models.CharField(max_length=100)
    voucher_number = models.CharField(max_length=20, unique=True, default='')
    cheque_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.description} ({self.amount})"

    def save(self, *args, **kwargs):
    # Set a default value for votehead
        votehead = self.votehead

        if self.payment_type == 'cash':
            self.cheque_number = None
            # Deduct cash amount from OperationsCashAccount
            bank_account = votehead.account
            cash_account = OperationsCashAccount.objects.first()
            if bank_account.account_number == cash_account.account_number:
                cash_account.cash_balance -= self.amount
                cash_account.total_balance = cash_account.cash_balance
                cash_account.save()
        else:
            # Deduct cheque amount from OperationsChequeAccount
            bank_account = votehead.account
            cheque_account = OperationsBankAccount.objects.first()
            if bank_account.account_number == cheque_account.account_number:
                cheque_account.bank_balance -= self.amount
                cheque_account.total_balance = cheque_account.bank_balance
                cheque_account.save()
                self.cheque_number = self.cheque_number

        super().save(*args, **kwargs)

    # Add the amount to the votehead
        votehead.amount_spent += self.amount
        votehead.balance = votehead.amount_budgeted - votehead.amount_spent
        votehead.save()



class Cheque(models.Model):
    payee_name = models.CharField(max_length=100)
    cheque_number = models.CharField(max_length=20, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_issued = models.DateField()
    votehead = models.ForeignKey(VoteHead, on_delete=models.CASCADE, related_name='cheques', blank=True, null=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f'Cheque {self.cheque_number} issued to {self.payee_name} on {self.date_issued}'

    def save(self, *args, **kwargs):
        # Check if there's a payment voucher with the same cheque number
        try:
            voucher = PaymentVoucher.objects.get(cheque_number=self.cheque_number)
        except PaymentVoucher.DoesNotExist:
            voucher = None

        if voucher:
            # Link the voucher to the cheque
            self.votehead = voucher.votehead

            # Deduct cheque amount from the votehead account
            votehead = voucher.votehead
            votehead.amount_spent += self.amount
            votehead.balance = votehead.amount_budgeted - votehead.amount_spent
            votehead.save()
        else:
            # Deduct cheque amount from the OperationsChequeAccount
            cheque_account = OperationsBankAccount.objects.first()
            cheque_account.bank_balance -= self.amount
            cheque_account.total_balance = cheque_account.bank_balance
            cheque_account.save()

        super().save(*args, **kwargs)





