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

    # Set the budget amount for each votehead to 0 initially
    budget_amounts = {votehead: Decimal('0') for votehead in voteheads}

    # Calculate the total budget amount and the budget amounts for each votehead
    total_budget_amount = Decimal('0')
    for votehead in voteheads:
        # Check if there are payment vouchers or cheques attached to this votehead for the given month and year
        if payment_vouchers.filter(votehead=votehead).exists() or cheques.filter(votehead=votehead).exists():
            max_budget_amount = cheque_receipt.amount - total_budget_amount
            budget_amount = Decimal(str(random.uniform(0, float(max_budget_amount))))
            budget_amount = budget_amount.quantize(Decimal('1.'), rounding='ROUND_DOWN')
            budget_amount = Decimal(budget_amount).quantize(Decimal('0.01'))
            budget_amount = round(budget_amount, -3)

            budget_amounts[votehead] = budget_amount
            total_budget_amount += budget_amount

    # If the total budget amount is less than the cheque receipt amount, add the difference to one of the budget amounts
    difference = cheque_receipt.amount - total_budget_amount
    if difference > 0:
        voteheads_with_budgets = [votehead for votehead, budget_amount in budget_amounts.items() if budget_amount > 0]
        if len(voteheads_with_budgets) > 0:
            votehead = random.choice(voteheads_with_budgets)
            budget_amounts[votehead] += difference
            budget_amounts[votehead] = budget_amounts[votehead].quantize(Decimal('0.01'))

    # Update the operations budgets and votehead receipts for each votehead
    my_account = OperationsBankAccount.objects.first()
    for votehead, budget_amount in budget_amounts.items():
        if budget_amount > 0:
            # Get or create the operations budget for this votehead and month
            budget, created = OperationsBudget.objects.get_or_create(
                votehead=votehead,
                account=my_account,
                date_budgeted=datetime(year=year, month=month, day=1),
                defaults={'amount': Decimal('0'), 'cheque_receipt': cheque_receipt}
            )

            # If the budget was not created, update its amount
            if not created:
                budget.amount = budget_amount
                budget.save()

            # Create or update the votehead receipt for this votehead and month
            votehead_receipt, _ = VoteHeadReceipt.objects.get_or_create(
                votehead=votehead,
                date_received=datetime(year=year, month=month, day=1),
                defaults={'amount': Decimal('0')}
            )
            votehead_receipt.amount += budget_amount
            votehead_receipt.amount = votehead_receipt.amount.quantize(Decimal('0.01'))
            votehead_receipt.save()

