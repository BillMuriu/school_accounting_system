from django.contrib import admin
from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(OperationsBankAccount)
admin.site.register(OperationsCashAccount)
admin.site.register(VoteHead)
admin.site.register(OperationsChequeReceipt)
admin.site.register(OperationsCashReceipt)
admin.site.register(PettyCash)
admin.site.register(OperationsBudget)
admin.site.register(VoteHeadReceipt)
admin.site.register(PaymentVoucher)
admin.site.register(Cheque)