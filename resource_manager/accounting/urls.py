from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('operations/', operations, name='operations'),
    path('receipts/', receipts, name='receipts'),
    # path('receipts/<int:receipt_id>/', receipt_detail, name='receipt_detail')
    path('receipts/<str:receipt_type>/<int:receipt_id>/', receipt_detail, name='receipt_detail'),
    path('receipts/cheque/create/', create_cheque_receipt, name='create_cheque_receipt'),
]
