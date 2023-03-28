from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *

# Create your views here.

def home(request):
    # Get the latest cheque receipt
    try:
        latest_receipt = OperationsChequeReceipt.objects.latest('date_received')
    except OperationsChequeReceipt.DoesNotExist:
        latest_receipt = None

    # Get all the cash receipts
    cash_receipts = OperationsCashReceipt.objects.all()

    # Get all the votehead objects
    voteheads = VoteHead.objects.all()

    # Get all the payment vouchers with cash as the payment type
    payment_vouchers = PaymentVoucher.objects.all()

    context = {
        'latest_receipt': latest_receipt,
        'voteheads': voteheads,
        'checkreceipts': OperationsChequeReceipt.objects.all(),
        'payment_vouchers': payment_vouchers,
        'cashreceipts': cash_receipts,
    }

    return render(request, 'accounting/cashbook.html', context)








