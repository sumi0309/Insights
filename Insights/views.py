from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def weather_page(request):
    return render(request, 'weather.html')

def get_weather(request):
    if request.method == 'POST':
        location = request.POST.get('location')
        return HttpResponse(f"Location entered: {location}")
    return HttpResponse("Invalid request method.")
