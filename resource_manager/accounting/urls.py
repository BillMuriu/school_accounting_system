from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('operations/', operations, name='operations'),

    #receipts
    path('receipts/', receipts, name='receipts'),
    path('receipts/<str:receipt_type>/<int:receipt_id>/', receipt_detail, name='receipt_detail'),
    path('receipts/cheque/create/', create_cheque_receipt, name='create_cheque_receipt'),

    #Budgeting
    path('vote_head_budget/', vote_head_budget, name='vote_head_budget'),
    path('budgets/<int:budget_id>/', budget_detail, name='budget_detail'),
    path('create_budget/', create_votehead_budget, name='create_budget'),

    #PettyCash
    path('pettycash/', pettycash_list, name='pettycash_list'),
    path('pettycash/<int:pk>/', pettycash_detail, name='pettycash_detail'),
    path('pettycash/create/', create_pettycash, name='create_pettycash'),

    #PaymentVoucher
    path('payment-vouchers/', payment_voucher_list, name='payment_voucher_list'),
    path('paymentvoucher/<int:pk>/', paymentvoucher_detail, name='paymentvoucher_detail'),
    path('paymentvoucher/create/', create_paymentvoucher, name='create_paymentvoucher'),

    #cheque
    path('cheques/', cheque_list, name='cheque_list'),
    path('cheques/<int:cheque_id>/', cheque_detail, name='cheque_detail'),
    path('cheques/create/', create_cheque, name='create_cheque'),

    #cashbook
    path('cashbook/', cashbook, name='cashbook'),

    #My url
    path('my-url/', my_view, name='my_view'),


]
