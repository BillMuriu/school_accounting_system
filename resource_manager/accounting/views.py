from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *

# Create your views here.

def home(request):
    # Get the latest cheque receipt
    latest_receipt = OperationsChequeReceipt.objects.latest('date_received')

    # Get the latest cash receipt
    latest_cash_receipt = OperationsCashReceipt.objects.latest('date_received')

    # Get all the votehead objects
    voteheads = VoteHead.objects.all()

    context = {
        'latest_receipt': latest_receipt,
        'latest_cash_receipt': latest_cash_receipt,
        'voteheads': voteheads,
        'checkreceipts': OperationsChequeReceipt.objects.all(),
        'cashreceipts': OperationsCashReceipt.objects.all()
    }

    return render(request, 'accounting/cashbook.html', context)





