import random
from datetime import datetime
from django.db.models import Sum
from django.utils import timezone
from .models import *

def update_voteheadreceipts():
    # Get the current month and year
    current_month = datetime.now().month
    current_year = datetime.now().year

    # Get the operation cheque receipt for the current month and year
    cheque_receipts = OperationsChequeReceipt.objects.filter(date_received__year=current_year, date_received__month=current_month)

    if not cheque_receipts:
        return

    # Get or create the operations budget for this account
    for receipt in cheque_receipts:
        try:
            budget = OperationsBudget.objects.get(account=receipt.account, date_budgeted__year=current_year, date_budgeted__month=current_month)
        except OperationsBudget.DoesNotExist:
            budget = OperationsBudget(
                account=receipt.account,
                amount=0,
                date_budgeted=timezone.now()
            )
        budget.save()

        # Calculate the budget amount for this receipt
        max_budget_amount = receipt.amount
        budget_amount = random.uniform(0, max_budget_amount)

        # Update the operations budget amount for this receipt
        budget.amount += budget_amount
        budget.save()

        # Create or update the votehead receipt for this account and month
        votehead_receipt, _ = VoteHeadReceipt.objects.get_or_create(
            account=receipt.account,
            date_received__year=current_year,
            date_received__month=current_month,
            defaults={'amount': 0}
        )
        votehead_receipt.amount += budget_amount
        votehead_receipt.save()
