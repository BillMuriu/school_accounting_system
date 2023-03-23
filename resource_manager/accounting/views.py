from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *

# Create your views here.

def home(request):
    # your view code here
    return HttpResponse("Hello, World!")


#adding money to the operation account
# def add_to_operations(request):
#     if request.method == 'POST':
#         form = OperationsTransactionForm(request.POST)
#         if form.is_valid():
#             account_number = form.cleaned_data['account_number']
#             amount = form.cleaned_data['amount']
#             transaction_number = form.cleaned_data['transaction_number']
#             transaction_type = form.cleaned_data['transaction_type']
#             payment_type = form.cleaned_data['payment_type']

#             account = OperationsAccount.objects.get(account_number=account_number)
#             account.balance += float(amount)
#             account.save()

#             transaction = OperationsTransaction.objects.create(
#                 account=account,
#                 transaction_number=transaction_number,
#                 transaction_type=transaction_type,
#                 amount=float(amount),
#                 payment_type=payment_type
#             )
#             transaction.save()

#             return HttpResponse(f"Added {amount} to {account_number} in {payment_type}")
#     else:
#         form = OperationsTransactionForm()
#     return render(request, 'add_to_operations.html', {'form': form})
