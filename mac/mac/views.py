from django.http import HttpResponse
from django.shortcuts import render
import datetime

# Create your views here.


def index(request):
    return render(request, 'index.html')
