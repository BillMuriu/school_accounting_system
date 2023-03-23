from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import OperationsAccount

# Create your views here.

def home(request):
    # your view code here
    return HttpResponse("Hello, World!")

def debit_operations_account(request):
    if request.method == 'POST':
        account_number = request.POST['account_number']
        amount = request.POST['amount']
        account = OperationsAccount.objects.get(account_number=account_number)
        account.balance -= amount
        account.save()
        return redirect('operations_account_detail', account_number=account_number)
    else:
        return render(request, 'debit_operations_account.html')
