from django.contrib import admin
from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(OperationsAccount)
admin.site.register(VoteHead)
admin.site.register(OperationsChequeReceipt)
admin.site.register(OperationsBudget)
admin.site.register(VoteHeadReceipt)
admin.site.register(PaymentVoucher)
admin.site.register(Cheque)