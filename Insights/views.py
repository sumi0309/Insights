from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def weather_page(request):
    return render(request, 'weather.html')

