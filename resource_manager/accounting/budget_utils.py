import random
from datetime import datetime

from django.db.models import Sum
from django.utils import timezone

from .models import OperationsChequeReceipt, OperationsBudget, VoteHeadReceipt, VoteHead

def update_voteheadreceipts():
    # Get the current month and year
    current_month = datetime.now().month
    current_year = datetime.now().year

    # Get all the cheque receipts for the current month and year
    cheque_receipts = OperationsChequeReceipt.objects.filter(date_received__year=current_year, date_received__month=current_month)

    # Group the cheque receipts by votehead
    grouped_cheque_receipts = {}
    for receipt in cheque_receipts:
        votehead = receipt.operationsbudget_set.first().votehead
        if votehead in grouped_cheque_receipts:
            grouped_cheque_receipts[votehead].append(receipt)
        else:
            grouped_cheque_receipts[votehead] = [receipt]

    # Create the operations budgets and update the votehead receipts
    for votehead, receipts in grouped_cheque_receipts.items():
        # Calculate the total amount of all the cheque receipts for this votehead
        total_amount = sum(receipt.amount for receipt in receipts)

        # Create the operations budget for this votehead
        budget = OperationsBudget(
            account=receipts[0].account,
            cheque_receipt=receipts[0],
            votehead=votehead,
            amount=0,
            date_budgeted=timezone.now()
        )
        budget.save()

        # Update the budget amount for each receipt and create/update the votehead receipt
        for receipt in receipts:
            # Generate a random budget amount for this receipt
            max_budget_amount = receipt.amount
            budget_amount = random.uniform(0, max_budget_amount)

            # Update the operations budget amount for this receipt
            budget.amount += budget_amount
            budget.save()

            # Create or update the votehead receipt for this votehead and month
            votehead_receipt, _ = VoteHeadReceipt.objects.get_or_create(
                votehead=votehead,
                date_received__year=current_year,
                date_received__month=current_month,
                defaults={'amount': 0}
            )
            votehead_receipt.amount += budget_amount
            votehead_receipt.save()

        # Ensure the total operations budget amount equals the total amount of all the cheque receipts for this votehead
        budget_total_amount = OperationsBudget.objects.filter(votehead=votehead, date_budgeted__year=current_year, date_budgeted__month=current_month).aggregate(Sum('amount'))['amount__sum']
        if budget_total_amount != total_amount:
            budget.amount += total_amount - budget_total_amount
            budget.save()
