from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *

# Create your views here.

def home(request):
    # your view code here
    return render(request, 'accounting/cashbook.html')


