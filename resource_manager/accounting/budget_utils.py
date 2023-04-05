import random
from decimal import Decimal
import decimal
from datetime import datetime
from django.db.models import Sum
from django.utils import timezone
from .models import *


def update_voteheadreceipts(month, year):
    # Get the cheque receipts for the given month and year
    try:
        cheque_receipt = OperationsChequeReceipt.objects.get(date_received__year=year, date_received__month=month)
    except OperationsChequeReceipt.DoesNotExist:
        # If no cheque receipts found, return without doing anything
        return

    # Get all the payment vouchers for the given month and year
    payment_vouchers = PaymentVoucher.objects.filter(date__year=year, date__month=month)

    # Get all the cheques for the given month and year
    cheques = Cheque.objects.filter(date_issued__year=year, date_issued__month=month)

    # Get all the unique voteheads associated with payment vouchers and cheques for the given month and year
    voteheads = set()
    for pv in payment_vouchers:
        if pv.votehead:
            voteheads.add(pv.votehead)
    for ch in cheques:
        if ch.votehead:
            voteheads.add(ch.votehead)

    # Update the operations budgets and votehead receipts for each votehead
    total_budget_amount = 0
    for votehead in voteheads:
        # Get or create the operations budget for this votehead and month
        my_account = OperationsBankAccount.objects.first()

        budget, created = OperationsBudget.objects.get_or_create(
            votehead=votehead,
            account=my_account,
            date_budgeted=datetime(year=year, month=month, day=1),
            defaults={'amount': 0, 'cheque_receipt': cheque_receipt}
        )

        # If the budget was not created, update its amount
        if not created:
            max_budget_amount = cheque_receipt.amount - total_budget_amount
            budget_amount = decimal.Decimal(str(random.uniform(0, float(max_budget_amount))))
            budget.amount = budget_amount.quantize(decimal.Decimal('1.'), rounding=decimal.ROUND_DOWN)
            budget.save()
            total_budget_amount += budget.amount

        # Create or update the votehead receipt for this votehead and month
        votehead_receipt, _ = VoteHeadReceipt.objects.get_or_create(
            votehead=votehead,
            date_received=datetime(year=year, month=month, day=1),
            defaults={'amount': 0}
        )
        votehead_receipt.amount += budget.amount
        votehead_receipt.save()
def update_voteheadreceipts(month, year):
    # Get the cheque receipts for the given month and year
    try:
        cheque_receipt = OperationsChequeReceipt.objects.get(date_received__year=year, date_received__month=month)
    except OperationsChequeReceipt.DoesNotExist:
        # If no cheque receipts found, return without doing anything
        return

    # Get all the payment vouchers for the given month and year
    payment_vouchers = PaymentVoucher.objects.filter(date__year=year, date__month=month)

    # Get all the cheques for the given month and year
    cheques = Cheque.objects.filter(date_issued__year=year, date_issued__month=month)

    # Get all the unique voteheads associated with payment vouchers and cheques for the given month and year
    voteheads = set()
    for pv in payment_vouchers:
        if pv.votehead:
            voteheads.add(pv.votehead)
    for ch in cheques:
        if ch.votehead:
            voteheads.add(ch.votehead)

    # Update the operations budgets and votehead receipts for each votehead
    total_budget_amount = 0
    for votehead in voteheads:
        # Get or create the operations budget for this votehead and month
        my_account = OperationsBankAccount.objects.first()

        budget, created = OperationsBudget.objects.get_or_create(
            votehead=votehead,
            account=my_account,
            date_budgeted=datetime(year=year, month=month, day=1),
            defaults={'amount': 0, 'cheque_receipt': cheque_receipt}
        )

        # If the budget was not created, update its amount
        if not created:
            max_budget_amount = cheque_receipt.amount - total_budget_amount
            budget_amount = decimal.Decimal(str(random.uniform(0, float(max_budget_amount))))
            budget.amount = budget_amount.quantize(decimal.Decimal('1.'), rounding=decimal.ROUND_DOWN)
            budget.save()
            total_budget_amount += budget.amount

        # Create or update the votehead receipt for this votehead and month
        votehead_receipt, _ = VoteHeadReceipt.objects.get_or_create(
            votehead=votehead,
            date_received=datetime(year=year, month=month, day=1),
            defaults={'amount': 0}
        )
        votehead_receipt.amount += budget.amount
        votehead_receipt.save()

