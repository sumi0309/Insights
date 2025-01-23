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
    """Handles form submission, constructs API request URL, sends request, and displays location options."""
    if request.method == 'POST':
        location = request.POST.get('location')

        encoded_location = urllib.parse.quote(location)

        api_url = f"{BASE_URL}{encoded_location}&api_key={API_KEY}"

        try:
            response = requests.get(api_url)

            if response.status_code == 200:
                data = response.json()

                display_names = [item["display_name"] for item in data]

                return JsonResponse({"display_names": display_names}, safe=False)
            else:
                return HttpResponse(f"Error fetching data. Status code: {response.status_code}", status=response.status_code)

        except requests.exceptions.RequestException as e:
            return HttpResponse(f"API request failed: {e}", status=500)

    return HttpResponse("Invalid request method.", status=400)

def select_location(request):
    """Receives user-selected display_name and finds the corresponding object."""
    if request.method == 'POST':
        selected_display_name = request.POST.get('selected_display_name')

        if not selected_display_name:
            return HttpResponse("No location selected.", status=400)

        encoded_location = urllib.parse.quote(selected_display_name)
        api_url = f"{BASE_URL}{encoded_location}&api_key={API_KEY}"

        try:
            response = requests.get(api_url)

            if response.status_code == 200:
                data = response.json()

                selected_object = next((item for item in data if item["display_name"] == selected_display_name), None)

                if selected_object:
                    return JsonResponse(selected_object, safe=False)
                else:
                    return HttpResponse("Selected location not found.", status=404)

            else:
                return HttpResponse(f"Error fetching data. Status code: {response.status_code}", status=response.status_code)

        except requests.exceptions.RequestException as e:
            return HttpResponse(f"API request failed: {e}", status=500)

    return HttpResponse("Invalid request method.", status=400)
