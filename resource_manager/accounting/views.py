from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *

# Create your views here.

def home(request):
    # Get the latest cheque receipt
    latest_receipt = OperationsChequeReceipt.objects.latest('date_received')

    # Get the cash account balance
    cash_account = OperationsCashAccount.objects.first()
    cash_balance = cash_account.cash_balance

    # Get the RMI votehead budgeted amount
    rmi_votehead = VoteHead.objects.get(name='Repairs Maintenance and Improvement')
    rmi_budgeted_amount = rmi_votehead.amount_budgeted

    # Get the Personal Emolument votehead budgeted amount
    pe_votehead = VoteHead.objects.get(name='Personal Emolument')
    pe_budgeted_amount = pe_votehead.amount_budgeted

    context = {
        'latest_receipt': latest_receipt,
        'cash_balance': cash_balance,
        'bank': latest_receipt.amount,
        'rmi_budgeted_amount': rmi_budgeted_amount,
        'pe_budgeted_amount': pe_budgeted_amount,
        'receipts': OperationsChequeReceipt.objects.all()
    }

    return render(request, 'accounting/cashbook.html', context)



