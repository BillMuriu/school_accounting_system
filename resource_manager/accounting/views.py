from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import *
from .budget_utils import update_voteheadreceipts
from datetime import datetime, timedelta
from django.core.cache import cache



# Create your views here.

def home(request):
    return render(request, 'accounting/home.html')


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
        cheque_receipt = form.save()
        return redirect('receipt_detail', receipt_type='cheque', receipt_id=cheque_receipt.id)

    context = {
        'form': form,
    }
    return render(request, 'accounting/create_cheque_receipt.html', context)


#Budgeting
def vote_head_budget(request):
    budgets = OperationsBudget.objects.all()
    context = {
        'budgets': budgets
    }
    return render(request, 'accounting/vote_head_budget.html', context)


#Budget Detail
def budget_detail(request, budget_id):
    budget = get_object_or_404(OperationsBudget, id=budget_id)
    context = {
        'budget': budget,
    }
    return render(request, 'accounting/budget_detail.html', context)


#Create budget view
def create_votehead_budget(request):
    if request.method == 'POST':
        form = OperationsBudgetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vote_head_budget')
    else:
        form = OperationsBudgetForm()
    context = {'form': form}
    return render(request, 'accounting/create_votehead_budget.html', context)


#PettyCash
def pettycash_list(request):
    pettycash = PettyCash.objects.all()
    context = {'pettycash': pettycash}
    return render(request, 'accounting/pettycash_list.html', context)


#PettyCashDetail
def pettycash_detail(request, pk):
    pettycash = get_object_or_404(PettyCash, pk=pk)
    context = {'pettycash': pettycash}
    return render(request, 'accounting/pettycash_detail.html', context)


#Create PettyCash
def create_pettycash(request):
    if request.method == 'POST':
        form = PettyCashForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pettycash_list')
    else:
        form = PettyCashForm()
    context = {'form': form}
    return render(request, 'accounting/create_pettycash.html', context)


#PaymentVoucher
def payment_voucher_list(request):
    vouchers = PaymentVoucher.objects.all()
    context = {'vouchers': vouchers}
    return render(request, 'accounting/payment_voucher_list.html', context)


#PaymentVoucher Detail
def paymentvoucher_detail(request, pk):
    paymentvoucher = get_object_or_404(PaymentVoucher, pk=pk)
    context = {'paymentvoucher': paymentvoucher}
    return render(request, 'accounting/paymentvoucher_detail.html', context)


#Create PaymentVoucher
def create_paymentvoucher(request):
    if request.method == 'POST':
        form = PaymentVoucherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payment_voucher_list')
    else:
        form = PaymentVoucherForm()
    context = {'form': form}
    return render(request, 'accounting/create_paymentvoucher.html', context)


#The cheques
def cheque_list(request):
    cheques = Cheque.objects.all()
    context = {'cheques': cheques}
    return render(request, 'accounting/cheque_list.html', context)


#The cheque detail
def cheque_detail(request, cheque_id):
    cheque = get_object_or_404(Cheque, id=cheque_id)
    context = {
        'cheque': cheque,
    }
    return render(request, 'accounting/cheque_detail.html', context)


# The create cheque view
def create_cheque(request):
    if request.method == 'POST':
        form = ChequeForm(request.POST)
        if form.is_valid():
            cheque = form.save()
            return redirect('cheque_detail', cheque_id=cheque.pk)
    else:
        form = ChequeForm()
    context = {
        'form': form,
    }
    return render(request, 'accounting/create_cheque.html', context)


#The Cashbook
def cashbook(request):
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



#What I need
def my_view(request):
    # Get the current date
    current_date = datetime.now()

    # Calculate the previous month and year
    previous_date = current_date - timedelta(days=current_date.day)
    previous_month = previous_date.month
    previous_year = previous_date.year

    # Get the cached values of the votehead budgets and cheque receipts, or calculate and cache them if they don't exist
    votehead_budgets = cache.get(f'votehead_budgets_{previous_month}_{previous_year}')
    cheque_receipts = cache.get(f'cheque_receipts_{previous_month}_{previous_year}')
    if not votehead_budgets or not cheque_receipts:
        # Update the votehead budgets for the previous month and year
        update_voteheadreceipts(previous_month, previous_year)

        # Get all the cheque receipts for the previous month and year
        cheque_receipts = OperationsChequeReceipt.objects.filter(date_received__year=previous_year, date_received__month=previous_month)

        # Get the votehead budgets for the previous month and year
        votehead_budgets = OperationsBudget.objects.filter(date_budgeted__year=previous_year, date_budgeted__month=previous_month)

        # Cache the values
        cache.set(f'votehead_budgets_{previous_month}_{previous_year}', votehead_budgets)
        cache.set(f'cheque_receipts_{previous_month}_{previous_year}', cheque_receipts)

    # Pass the cached values of the cheque_receipts and votehead_budgets to the template
    context = {
        'cheque_receipts': cheque_receipts,
        'votehead_budgets': votehead_budgets
    }
    return render(request, 'accounting/my_template.html', context)







