import random
from decimal import Decimal
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

    # Compute the total amount available for budgeting
    total_budget_amount = cheque_receipt.amount

    # Distribute the total budget amount randomly among the voteheads
    votehead_budget_amounts = {}
    for votehead in voteheads:
        # Calculate the maximum budget amount for this votehead
        votehead_max_budget_amount = Decimal('0')
        for pv in payment_vouchers.filter(votehead=votehead):
            votehead_max_budget_amount += pv.amount
        for ch in cheques.filter(votehead=votehead):
            votehead_max_budget_amount += ch.amount

        # Calculate the budget amount for this votehead as a random amount up to the maximum budget amount
        if total_budget_amount > 0:
            votehead_budget_amount = Decimal(str(random.uniform(0, float(votehead_max_budget_amount))))
            votehead_budget_amount = votehead_budget_amount.quantize(Decimal('1.'), rounding='ROUND_DOWN')
            if votehead_budget_amount > total_budget_amount:
                votehead_budget_amount = total_budget_amount
            total_budget_amount -= votehead_budget_amount
        else:
            votehead_budget_amount = Decimal('0')

        votehead_budget_amounts[votehead] = votehead_budget_amount

    # Update the operations budgets and votehead receipts for each votehead
    for votehead in voteheads:
        # Get or create the operations budget for this votehead and month
        my_account = OperationsBankAccount.objects.first()

        budget, created = OperationsBudget.objects.get_or_create(
            votehead=votehead,
            account=my_account,
            date_budgeted=datetime(year=year, month=month, day=1),
            defaults={'amount': Decimal('0'), 'cheque_receipt': cheque_receipt}
        )

        # If the budget was not created, update its amount
        if not created:
            budget_amount = votehead_budget_amounts[votehead]
            budget.amount = budget_amount
            budget.save()

        # Create or update the votehead receipt for this votehead and month
        votehead_receipt, _ = VoteHeadReceipt.objects.get_or_create(
            votehead=votehead,
            date_received=datetime(year=year, month=month, day=1),
            defaults={'amount': Decimal('0')}
        )
        votehead_receipt.amount += budget.amount
        votehead_receipt.save()

