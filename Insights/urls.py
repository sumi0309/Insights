"""
URL configuration for Insights project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views,weather,displayWeather

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('weather/', views.weather_page, name='weather_page'),
    path('get_weather/', weather.get_weather, name='get_weather'),
    path('select_location/', weather.select_location, name='select_location'),
    path('weather_display/', displayWeather.get_weather_data, name='weather_display'),
]
