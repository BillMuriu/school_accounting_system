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

    #Budgeting
    path('vote_head_budget/', vote_head_budget, name='vote_head_budget'),
    path('budgets/<int:budget_id>/', budget_detail, name='budget_detail'),
    path('create_budget/', create_votehead_budget, name='create_budget'),

    #PettyCash
    path('pettycash/', pettycash_list, name='pettycash_list'),
    path('pettycash/<int:pk>/', pettycash_detail, name='pettycash_detail'),


]
