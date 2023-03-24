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
#             account = form.cleaned_data['account']
#             amount = form.cleaned_data['amount']
#             payment_type = form.cleaned_data['payment_type']
#             votehead = form.cleaned_data['votehead']

#             account.cash_balance += float(amount) if payment_type == 'cash' else 0
#             account.bank_balance += float(amount) if payment_type != 'cash' else 0
#             account.total_balance = account.cash_balance + account.bank_balance
#             account.save()

#             transaction = OperationsTransaction.objects.create(
#                 account=account,
#                 votehead=votehead,
#                 amount=float(amount),
#                 payment_type=payment_type
#             )

#             context = {
#                 'message': f"Added {amount} to {account.account_number} in {payment_type}"
#             }
#             return render(request, 'add_to_operations.html', context)
#     else:
#         form = OperationsTransactionForm()
#     context = {
#         'form': form
#     }
#     return render(request, 'add_to_operations.html', context)


#add receipt




