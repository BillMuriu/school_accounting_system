from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
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


# Receipt Detail
def receipt_detail(request, receipt_type, receipt_id):
    if receipt_type == 'cash':
        receipt = OperationsCashReceipt.objects.filter(id=receipt_id).first()
        template = 'accounting/cash_receipt_detail.html'
    elif receipt_type == 'cheque':
        receipt = OperationsChequeReceipt.objects.filter(id=receipt_id).first()
        template = 'accounting/cheque_receipt_detail.html'
    else:
        raise Http404("Receipt type does not exist")
    
    if not receipt:
        raise Http404("Receipt does not exist")
    
    context = {
        'receipt': receipt,
        'receipt_type': receipt_type.capitalize() + ' Receipt',
    }
    
    return render(request, template, context)


# Create Cheque Receipt
def create_cheque_receipt(request):
    form = ChequeReceiptForm(request.POST or None)
    if form.is_valid():
        cheque_receipt = form.save(commit=False)
        cheque_receipt.save()

        return redirect('receipt_detail', receipt_type='cheque', receipt_id=cheque_receipt.id)

    context = {
        'form': form,
    }
    return render(request, 'accounting/create_cheque_receipt.html', context)










