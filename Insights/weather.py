from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import urllib.parse  
import requests  
from dotenv import load_dotenv
import os
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

load_dotenv()

API_KEY = os.getenv("API_KEY") 
BASE_URL = "https://geocode.maps.co/search?q="

cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

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
                    latitude = selected_object.get("lat")
                    longitude = selected_object.get("lon")
                    display_name = selected_object.get("display_name")

                    request.session['latitude'] = latitude
                    request.session['longitude'] = longitude
                    request.session['display_name'] = display_name

                    return JsonResponse({"success": True})

                else:
                    return HttpResponse("Selected location not found.", status=404)

            else:
                return HttpResponse(f"Error fetching data. Status code: {response.status_code}", status=response.status_code)

        except requests.exceptions.RequestException as e:
            return HttpResponse(f"API request failed: {e}", status=500)

    return HttpResponse("Invalid request method.", status=400)


def weather_display(request):
    """Fetch stored location data from session and display it."""
    latitude = request.session.get('latitude')
    longitude = request.session.get('longitude')
    display_name = request.session.get('display_name')

    if not latitude or not longitude or not display_name:
        return HttpResponse("No location data found in session. Please select a location first.", status=404)

    return render(request, 'displayWeather.html', {
        "latitude": latitude,
        "longitude": longitude,
        "display_name": display_name
    })



