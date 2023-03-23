from django.db import models

# Create your models here.

class OperationsAccount(models.Model):
    account_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=50)

    @property
    def cash_balance(self):
        cash_transactions = self.operationstransaction_set.filter(payment_type='cash')
        cash_debits = cash_transactions.filter(transaction_type='debit').aggregate(Sum('amount'))['amount__sum'] or 0
        cash_credits = cash_transactions.filter(transaction_type='credit').aggregate(Sum('amount'))['amount__sum'] or 0
        return cash_credits - cash_debits

    @property
    def bank_balance(self):
        bank_transactions = self.operationstransaction_set.exclude(payment_type='cash')
        bank_debits = bank_transactions.filter(transaction_type='debit').aggregate(Sum('amount'))['amount__sum'] or 0
        bank_credits = bank_transactions.filter(transaction_type='credit').aggregate(Sum('amount'))['amount__sum'] or 0
        return bank_credits - bank_debits

    @property
    def total_balance(self):
        return self.cash_balance + self.bank_balance

    def __str__(self):
        return self.name

    
class OperationsTransaction(models.Model):
    account = models.ForeignKey(OperationsAccount, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    payment_type = models.CharField(max_length=10, choices=[('cash', 'Cash'), ('cheque', 'Cheque')])

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"


