from django.shortcuts import render, redirect
from django.http import Http404
from django.shortcuts import render, get_object_or_404
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


# The DashBoard
def dashboard(request):
    return render(request, 'accounting/dashboard.html')


#Operations
def operations(request):
    return render(request, 'accounting/operations.html')


#Receipts
def receipts(request):
    cash_receipts = OperationsCashReceipt.objects.all()
    bank_receipts = OperationsChequeReceipt.objects.all()

    context = {
        'cash_receipts': cash_receipts,
        'bank_receipts': bank_receipts,
    }

    return render(request, 'accounting/receipts.html', context)


#Receipt Detail
def receipt_detail(request, receipt_id):
    try:
        cash_receipt = OperationsCashReceipt.objects.get(id=receipt_id)
        context = {
            'receipt': cash_receipt,
            'receipt_type': 'Cash Receipt',
        }
        template = 'accounting/cash_receipt_detail.html'
    except OperationsCashReceipt.DoesNotExist:
        try:
            cheque_receipt = OperationsChequeReceipt.objects.get(id=receipt_id)
            context = {
                'receipt': cheque_receipt,
                'receipt_type': 'Cheque Receipt',
            }
            template = 'accounting/cheque_receipt_detail.html'
        except OperationsChequeReceipt.DoesNotExist:
            raise Http404("Receipt does not exist")
        
    return render(request, template, context)










