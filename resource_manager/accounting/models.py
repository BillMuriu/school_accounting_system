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

    def __str__(self):
        return self.name


class OperationsChequeReceipt(models.Model):
    account = models.ForeignKey(OperationsAccount, on_delete=models.CASCADE, default=None)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_received = models.DateField()

    def __str__(self):
        return f"Cheque receipt {self.id} for {self.account.account_number}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        account = self.account
        amount = self.amount

        account.bank_balance += amount
        account.total_balance = account.cash_balance + account.bank_balance
        account.save()





class VoteHead(models.Model):
    ACCOUNT_TYPES = (
        ('operations', 'Operations Account'),
        ('other', 'Other Account'),
    )

    name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, default='other')
    account_number = models.CharField(max_length=20, unique=True, default='')
    account = models.ForeignKey(OperationsAccount, on_delete=models.CASCADE, default=None)
    amount_budgeted = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class OperationsBudget(models.Model):
    account = models.ForeignKey(OperationsAccount, on_delete=models.CASCADE)
    votehead = models.ForeignKey(VoteHead, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_budgeted = models.DateField()

    def __str__(self):
        return f"{self.votehead} budgeted {self.amount} for {self.account.account_number}"

    def save(self, *args, **kwargs):
        # Update account balance
        account = self.account
        votehead_amount = self.amount
        if account.total_balance < votehead_amount:
            raise ValueError(f"Insufficient funds in account {account.account_number}")
        if account.bank_balance >= votehead_amount:
            account.bank_balance -= votehead_amount
        else:
            account.cash_balance -= votehead_amount - account.bank_balance
            account.bank_balance = 0
        account.total_balance = account.cash_balance + account.bank_balance
        account.save()

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
        if self.payment_type == 'cash':
            self.cheque_number = None
        super().save(*args, **kwargs)

        # Deduct the amount from the votehead
        votehead = self.votehead
        votehead.amount_budgeted -= self.amount
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








