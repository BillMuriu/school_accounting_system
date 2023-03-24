from django.db import models
from django.db.models import Sum

# Create your models here.

class OperationsAccount(models.Model):
    account_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=50)
    cash_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bank_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

class OperationsReceipt(models.Model):
    account = models.ForeignKey(OperationsAccount, on_delete=models.CASCADE, default=None)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    receipt_type = models.CharField(max_length=10, choices=[('cash', 'Cash'), ('cheque', 'Cheque')])
    date_received = models.DateField()

    def __str__(self):
        return f"Receipt {self.id} for {self.account.account_number} ({self.receipt_type})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        account = self.account
        amount = self.amount
        receipt_type = self.receipt_type

        if receipt_type == 'cash':
            account.cash_balance += amount
        elif receipt_type == 'cheque':
            account.bank_balance += amount

        account.total_balance = account.cash_balance + account.bank_balance
        account.save()




class Votehead(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class OperationsBudget(models.Model):
    account = models.ForeignKey(OperationsAccount, on_delete=models.CASCADE)
    votehead = models.ForeignKey(Votehead, on_delete=models.CASCADE)
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
        if account.cash_balance >= votehead_amount:
            account.cash_balance -= votehead_amount
        else:
            account.bank_balance -= votehead_amount - account.cash_balance
            account.cash_balance = 0
        account.total_balance = account.cash_balance + account.bank_balance
        account.save()

        # Save budget
        super().save(*args, **kwargs)








