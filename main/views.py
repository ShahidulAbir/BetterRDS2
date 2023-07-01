from django.shortcuts import render
from django.shortcuts import render, redirect


# Create your views here.
def homepage(request):
    return render(request, 'main/homepage.html')
