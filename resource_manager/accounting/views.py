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

    # Get all the payment vouchers with cash as the payment type
    payment_vouchers = PaymentVoucher.objects.filter(payment_type='Cash')

    context = {
        'latest_receipt': latest_receipt,
        'latest_cash_receipt': latest_cash_receipt,
        'voteheads': voteheads,
        'checkreceipts': OperationsChequeReceipt.objects.all(),
        'payment_vouchers': payment_vouchers,
        'cashreceipts': OperationsCashReceipt.objects.all()
    }

    return render(request, 'accounting/cashbook.html', context)






