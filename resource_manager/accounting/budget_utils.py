import random
from datetime import datetime

from django.db.models import Sum
from django.utils import timezone

from .models import *

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

    # Create/update the operations budgets and update the votehead receipts
    for votehead, receipts in grouped_cheque_receipts.items():
        # Calculate the total amount of all the cheque receipts for this votehead
        total_amount = sum(receipt.amount for receipt in receipts)

        # Check if any payment vouchers or cheques for this votehead exist for this month
        if not (OperationsChequeReceipt.objects.filter(date_received__year=current_year, date_received__month=current_month, votehead__id=votehead.id).exists() or PaymentVoucher.objects.filter(date__year=current_year, date__month=current_month, votehead__id=votehead.id).exists()):
            continue

        # Get or create the operations budget for this votehead
        try:
            budget = OperationsBudget.objects.get(votehead=votehead, date_budgeted__year=current_year, date_budgeted__month=current_month)
        except OperationsBudget.DoesNotExist:
            budget = OperationsBudget(
                account=receipts[0].account,
                votehead=votehead,
                amount=0,
                date_budgeted=timezone.now()
            )
        budget.save()

        # Update the budget amount for each receipt and create/update the votehead receipt
        for receipt in receipts:
            # Check if the receipt is tied to this votehead
            if not receipt.operationsbudget_set.filter(votehead=votehead).exists():
                continue

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
            budget_ratio = total_amount / budget_total_amount
            for operations_budget in OperationsBudget.objects.filter(votehead=votehead, date_budgeted__year=current_year, date_budgeted__month=current_month):
                operations_budget.amount *= budget_ratio
                operations_budget.save()
