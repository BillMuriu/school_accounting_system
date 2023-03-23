from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *

# Create your views here.

def home(request):
    # your view code here
    return HttpResponse("Hello, World!")


#adding money to the operation account
def add_to_operations(request):
    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        amount = request.POST.get('amount')
        transaction_number = request.POST.get('transaction_number')
        transaction_type = request.POST.get('transaction_type')
        payment_type = request.POST.get('payment_type')

        account = OperationsAccount.objects.get(account_number=account_number)
        account.balance += float(amount)
        account.save()

        transaction = OperationsTransaction.objects.create(
            account=account,
            transaction_number=transaction_number,
            transaction_type=transaction_type,
            amount=float(amount),
            payment_type=payment_type
        )
        transaction.save()

        return HttpResponse(f"Added {amount} to {account_number} in {payment_type}")
    else:
        return render(request, 'add_to_operations.html')

