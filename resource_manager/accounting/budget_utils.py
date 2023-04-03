import random
from datetime import datetime
from django.db.models import Sum
from django.utils import timezone
from .models import *

def update_voteheadreceipts():
    # Get the current month and year
    current_month = datetime.now().month
    current_year = datetime.now().year

    # Get the cheque receipts for the current month and year
    try:
        cheque_receipt = OperationsChequeReceipt.objects.get(date_received__year=current_year, date_received__month=current_month)
    except OperationsChequeReceipt.DoesNotExist:
        # If no cheque receipts found, return without doing anything
        return

    # Get all the payment vouchers for the current month and year
    payment_vouchers = PaymentVoucher.objects.filter(date__year=current_year, date__month=current_month)

    # Get all the cheques for the current month and year
    cheques = Cheque.objects.filter(date__year=current_year, date__month=current_month)

    # Get all the unique voteheads associated with payment vouchers and cheques for the current month and year
    voteheads = set()
    for pv in payment_vouchers:
        if pv.vote_head:
            voteheads.add(pv.vote_head)
    for ch in cheques:
        if ch.vote_head:
            voteheads.add(ch.vote_head)

    # Create/update the operations budgets and update the votehead receipts
    total_budget_amount = 0
    for votehead in voteheads:
        # Get or create the operations budget for this votehead
        try:
            budget = OperationsBudget.objects.get(vote_head=votehead, date_budgeted__year=current_year, date_budgeted__month=current_month)
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
            date_received__year=current_year,
            date_received__month=current_month,
            defaults={'amount': 0}
        )
        votehead_receipt.amount += budget_amount
        votehead_receipt.save()
