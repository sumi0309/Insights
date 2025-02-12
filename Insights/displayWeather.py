import openmeteo_requests
import requests_cache
from retry_requests import retry
from django.shortcuts import render

# Setting up the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

def get_weather_data(request):
    # Retrieve latitude and longitude from the session
    latitude = request.session.get('latitude')
    longitude = request.session.get('longitude')

    if latitude is None or longitude is None:
        return JsonResponse({"error": "Latitude and Longitude not found in session"}, status=400)

    # Open-Meteo API endpoint and parameters
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ["temperature_2m", "apparent_temperature", "precipitation", "rain", "snowfall", "wind_speed_10m"],
        "daily": ["temperature_2m_max", "temperature_2m_min", "sunrise", "sunset"],
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "timezone": "GMT",
    }

    # Fetch weather data from Open-Meteo
    response = openmeteo.weather_api(url, params=params)
    current=response[0].Current()
    hourly=response[0].Hourly()
    daily=response[0].Daily()

    weather_data = {
        "current": {
            "temperature_2m": current.Variables(0).Value(),
            "feelsLike": current.Variables(1).Value(),
            "precipitation": current.Variables(2).Value(),
            "rain": current.Variables(3).Value(),
            "snowfall": current.Variables(4).Value(),
            "wind_speed_10m": current.Variables(5).Value(),
        },
        "daily": {
            "temperature_2m_max": daily.Variables(0).ValuesAsNumpy(),
            "temperature_2m_min": daily.Variables(1).ValuesAsNumpy(),
            "sunrise": daily.Variables(2).ValuesAsNumpy(),
            "sunset": daily.Variables(3).ValuesAsNumpy(),
        }
    }
    
    daily_temperatures = zip(weather_data['daily']['temperature_2m_max'], weather_data['daily']['temperature_2m_min'])

    return render(request, 'displayWeather.html', {
        "weather_data": weather_data,
        "daily_temp": daily_temperatures,
        "display_name": request.session.get("display_name", "Unknown"),
        "latitude": latitude,
        "longitude": longitude,
    })










# import openmeteo_requests

# import requests_cache
# import pandas as pd
# from retry_requests import retry

# # Setting up the Open-Meteo API client with cache and retry on error
# cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
# retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
# openmeteo = openmeteo_requests.Client(session = retry_session)

# url = "https://api.open-meteo.com/v1/forecast"
# params = {
# 	"latitude": 52.52,
# 	"longitude": 13.41,
# 	"current": ["temperature_2m", "apparent_temperature", "precipitation", "rain", "snowfall", "wind_speed_10m"],
# 	"hourly": ["temperature_2m", "apparent_temperature", "precipitation_probability", "rain", "snowfall", "snow_depth", "wind_speed_10m", "uv_index"],
# 	"daily": ["temperature_2m_max", "temperature_2m_min", "sunrise", "sunset"],
# 	"temperature_unit": "fahrenheit",
# 	"wind_speed_unit": "mph",
# 	"timezone": "GMT",
# 	"forecast_hours": 24
# }
# responses = openmeteo.weather_api(url, params=params)

# response = responses[0]
# print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
# print(f"Elevation {response.Elevation()} m asl")
# print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
# print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")


# current = response.Current()

# current_temperature_2m = current.Variables(0).Value()

# current_apparent_temperature = current.Variables(1).Value()

# current_precipitation = current.Variables(2).Value()

# current_rain = current.Variables(3).Value()

# current_snowfall = current.Variables(4).Value()

# current_wind_speed_10m = current.Variables(5).Value()

# print(f"Current time {current.Time()}")

# print(f"Current temperature_2m {current_temperature_2m}")
# print(f"Current apparent_temperature {current_apparent_temperature}")
# print(f"Current precipitation {current_precipitation}")
# print(f"Current rain {current_rain}")
# print(f"Current snowfall {current_snowfall}")
# print(f"Current wind_speed_10m {current_wind_speed_10m}")

# hourly = response.Hourly()
# hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
# hourly_apparent_temperature = hourly.Variables(1).ValuesAsNumpy()
# hourly_precipitation_probability = hourly.Variables(2).ValuesAsNumpy()
# hourly_rain = hourly.Variables(3).ValuesAsNumpy()
# hourly_snowfall = hourly.Variables(4).ValuesAsNumpy()
# hourly_snow_depth = hourly.Variables(5).ValuesAsNumpy()
# hourly_wind_speed_10m = hourly.Variables(6).ValuesAsNumpy()
# hourly_uv_index = hourly.Variables(7).ValuesAsNumpy()

# hourly_data = {"date": pd.date_range(
# 	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
# 	end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
# 	freq = pd.Timedelta(seconds = hourly.Interval()),
# 	inclusive = "left"
# )}

# hourly_data["temperature_2m"] = hourly_temperature_2m
# hourly_data["apparent_temperature"] = hourly_apparent_temperature
# hourly_data["precipitation_probability"] = hourly_precipitation_probability
# hourly_data["rain"] = hourly_rain
# hourly_data["snowfall"] = hourly_snowfall
# hourly_data["snow_depth"] = hourly_snow_depth
# hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
# hourly_data["uv_index"] = hourly_uv_index

# hourly_dataframe = pd.DataFrame(data = hourly_data)
# print(hourly_dataframe)


# daily = response.Daily()
# daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
# daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
# daily_sunrise = daily.Variables(2).ValuesAsNumpy()
# daily_sunset = daily.Variables(3).ValuesAsNumpy()

# daily_data = {"date": pd.date_range(
# 	start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
# 	end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
# 	freq = pd.Timedelta(seconds = daily.Interval()),
# 	inclusive = "left"
# )}

# daily_data["temperature_2m_max"] = daily_temperature_2m_max
# daily_data["temperature_2m_min"] = daily_temperature_2m_min
# daily_data["sunrise"] = daily_sunrise
# daily_data["sunset"] = daily_sunset

# daily_dataframe = pd.DataFrame(data = daily_data)
# print(daily_dataframe)