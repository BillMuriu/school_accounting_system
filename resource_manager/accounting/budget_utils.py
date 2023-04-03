import random
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

    # Create/update the operations budgets and update the votehead receipts
    total_budget_amount = 0
    for votehead in voteheads:
        # Get or create the operations budget for this votehead
        try:
            budget = OperationsBudget.objects.get(vote_head=votehead, date_budgeted__year=year, date_budgeted__month=month)
        except OperationsBudget.DoesNotExist:
            budget = OperationsBudget(
                vote_head=votehead,
                amount=0,
                date_budgeted=timezone.now()
            )
        budget.save()

        # Calculate the budget amount for this votehead
        max_budget_amount = cheque_receipt.amount - total_budget_amount
        budget_amount = random.uniform(0, max_budget_amount)

        # Update the operations budget amount for this votehead
        budget.amount += budget_amount
        budget.save()
        total_budget_amount += budget_amount

        # Create or update the votehead receipt for this votehead and month
        votehead_receipt, _ = VoteHeadReceipt.objects.get_or_create(
            vote_head=votehead,
            date_received__year=year,
            date_received__month=month,
            defaults={'amount': 0}
        )
        votehead_receipt.amount += budget_amount
        votehead_receipt.save()
