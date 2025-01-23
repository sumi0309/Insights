from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import urllib.parse  
import requests  
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY") 
BASE_URL = "https://geocode.maps.co/search?q="

def weather_page(request):
    """Renders the weather input page."""
    return render(request, 'weather.html')

def get_weather(request):
    """Handles form submission, constructs API request URL, sends request, and displays JSON response."""
    if request.method == 'POST':
        location = request.POST.get('location')

       
        encoded_location = urllib.parse.quote(location)

        
        api_url = f"{BASE_URL}{encoded_location}&api_key={API_KEY}"

        try:
           
            response = requests.get(api_url)

            
            if response.status_code == 200:
                data = response.json()
                return JsonResponse(data, safe=False)
            else:
                return HttpResponse(f"Error fetching data. Status code: {response.status_code}", status=response.status_code)

        except requests.exceptions.RequestException as e:
            return HttpResponse(f"API request failed: {e}", status=500)

    return HttpResponse("Invalid request method.", status=400)
