from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('operations/', operations, name='operations'),
    path('receipts/', receipts, name='receipts'),
    path('receipts/<int:receipt_id>/', receipt_detail, name='receipt_detail'),
]
