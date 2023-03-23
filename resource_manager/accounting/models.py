from django.db import models

# Create your models here.

class OperationsAccount(models.Model):
    account_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
class OperationsTransaction(models.Model):
    account = models.ForeignKey(OperationsAccount, on_delete=models.CASCADE)
    transaction_number = models.CharField(max_length=20)
    transaction_type = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    payment_type = models.CharField(max_length=10, choices=[('cash', 'Cash'), ('cheque', 'Cheque')])

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"


