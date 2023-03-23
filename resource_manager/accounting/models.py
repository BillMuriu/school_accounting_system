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


class Votehead(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class OperationsTransaction(models.Model):
    account = models.ForeignKey(OperationsAccount, on_delete=models.CASCADE)
    votehead = models.ForeignKey(Votehead, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    payment_type = models.CharField(max_length=10, choices=[('cash', 'Cash'), ('cheque', 'Cheque')])

    def __str__(self):
        return f"{self.votehead} - {self.amount}"


class OperationsReceipt(models.Model):
    account_number = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    receipt_type = models.CharField(max_length=10)
    date_received = models.DateField()

    def __str__(self):
        return f"Receipt {self.id} for {self.account_number}"



